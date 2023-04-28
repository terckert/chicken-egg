import random
import matplotlib.pyplot as plt
import numpy as np
import math

# Number of cycles to run the simulation for
cycles = 100

# Knobs that can be turned on individual nests
startingPop = 10                    # Starting population of a nest
maleChance = 0.40                   # Chance of male rooster hatching
chanceOfMovingIfNotBred = 0.50      # Chance that a chicken will leave the nest if can't breed
chanceFertilizedEgg = 0.50          # Chance that an egg will be fertilized in a cycle
startingAggression = 0.10           # Starting aggression rate, factors into fitness. At high 
                                    # aggression a chicken has a chance to kill another chicken
startingSpeed = 0.10                # Decreases the chance that a chicken will die crossing the
                                    # road
maxAge = 7                          # Age at which chickens die of natural causes
henFertileAge = 4                   # Age at which hens stop producing eggs. They are still 
                                    # factored into breeding controls, but cannot reproduce
hensImpregnatedPerRooster = 1       # Number of hens that a rooster can impregnate in a single cycle

# Fitness stats. Speed and aggression factor into a roosters chance to breed. The more
# fit a rooster is to breed, the more likely they will find mates. These are the weights
# applied to to the stat. Uses multiplication, if you want to reduce a stat, multiply it by
# smaller percentage
speedWeight = 1.00
aggressionWeight = 0.50


class Chicken():
    def __init__(self, agg, spd) -> None:
        self.aggression = agg   # Aggression level
        self.speed = spd        # Speed
        self.age = 0            # Age
        self.bred = 0           # Boolean, whether they bred this cycle or not
        self.alive = 1          # Boolean, whether they died crossing road

class Nest():
    def __init__(self, name, startingPop = 0):
        self.name  = name       # Name of the next
        
        self.roosters = []      # Male chicken array
        self.hens  = []         # Female chicken array
        self.roads = []         # List of adjacent nests and the danger of crossing the road
        self.travelers = []     # List of travelers and their destination
        
        global startingSpeed
        global startingAggression
        for i in range(startingPop):
            newChicken = Chicken(startingAggression, startingSpeed)
            self.roosters.append(newChicken) if random.random() < maleChance else self.hens.append(newChicken)

    def createRoad(self, name, danger): # Create a road and append to the roads list
        self.roads.append({
            "name": name                # Name of the adjacent nest
            , "danger": danger          # Danger of crossing the road
        })

    def clearTravelers(self):
        self.travelers = []
    
    def getTravelers(self):
        return self.travelers
    
    """
    In order to reduce runtime, we need to reduce the number of times the array is iterated. To do that we're
    using slices and pops to decide who is crossing, who isn't, and what road they're crossing.
    """
    def whyDidTheChickenCrossTheRoad(self, startingInd, gender):
        slicedList        = []
        stayingList       = []

        # Slice the list from the starting index to the end
        if (gender == "male"):
            slicedList = self.roosters[startingInd:]
            self.roosters = self.roosters[:startingInd]
        else:
            slicedList = self.hens[startingInd:]
            self.hens = self.hens[:startingInd]

        #print(f"Number of chickens running: {len(slicedList)}")
        currentRun = 0  # TODO: Remove after debugging
        # "How many roads must a chicken walk down before we can call them a chicken?"
        # Start running them across roads:
        while (len(slicedList) > 0):
            currentRun += 1 # TODO: Remove after debugging
            
            chicken = slicedList.pop()          # Pop the chicken from the list and use the decision tree
            if random.random() < chanceOfMovingIfNotBred: # This chicken is on the move!
                whichRoad = random.random()     # Chooses the road the chicken will cross
                chancePerRoad = 1/len(self.roads) # Figure out the chance that a path is taken
                
                # Say we have 5 roads, there's a .20 chance that any road will be chosen. We work backwards
                # to find out which road is chosen starting at len-1. 
                # 4*.20 = .8, 3*.2 = .6, 2*.2 = .4, 1*.2 = .2 , 0*.2 = 0... we can use this check to figure
                # out which path is taken. If we move forwards and the random number is greater than 0 and
                # they will always choose the first path.
                roadInd = len(self.roads) - 1
                
                # Figure out which road the chicken will walk down.
                while (float(roadInd) * chancePerRoad) > whichRoad:
                    roadInd -= 1
                
                # Does the chicken die?
                if random.random() > self.roads[roadInd]["danger"] - chicken.speed: # Faster chicken, less death
                    chicken.speed += 0.01       # Increase the speed because of experience

                    # Add to the traveler list, at the end of the cycle map controller will take the lists and 
                    # move chickens to where they belong.
                    self.travelers.append(      
                        {
                            "nest": self.roads[roadInd]["name"]
                            , "chicken": chicken
                        }
                    )
                    #print(f"{currentRun}: Chicken successfully ran away.") # TODO: Remove after debugging
                # else:
                    #print(f"{currentRun}: Chicken died!") # TODO: Remove after debugging
            else:
                stayingList.append(chicken)
                #print(f"{currentRun}: Chicken decided to stay.") # TODO: Remove after debugging

        if (gender == 'male'):
            self.roosters += stayingList
        else:
            self.hens += stayingList

        #print(self.getTravelers()) # TODO: Remove after debugging
        self.clearTravelers() # TODO: Remove after debugging
    

    def simulateNest(self, cycles):
        roosterArr  = [len(self.roosters)]
        henArr   = [len(self.hens)]
        totalArr = [len(self.roosters) +len(self.hens)]
        newRoosters = []
        newHens  = [] 

        for i in range(1, cycles + 1):
            # Kill the old ones
            self.roosters = [r for r in self.roosters if r.age < maxAge]
            self.hens  = [h for h in self.hens  if h.age < maxAge]

            # Aggression and speed determine the fitness of each rooster to procreate.
            # Aggression is taken at full value, while speed is halved
            # To randomize stat distribution, we randomly distribute the hens in the list
            # of hens.
            # TODO This may be fucked. Its probably sorting in ascending order so the gymbro
            # chickens ain't getting no play.
            self.roosters = sorted(
                self.roosters
                , key= lambda r: (r.aggression*aggressionWeight) + (r.speed*speedWeight)
                , reverse=True   
            )
            random.shuffle(self.hens)

            # Clear the list of next gen chickens
            newRoosters = []
            newHens = []

            # Clear the breeding variables
            # for r in self.roosters:
            #     r.bred = 0
            # for h in self.hens:
            #     h.bred = 0

            # Breed them. 
            for r in range(len(self.roosters)):
                # Check if enough hens exits to the rooster to breed with. If the length of the 
                # hens list is greater than rooster index * the number of hens the rooster can breed
                # with, we get our breed on. If we've exceeded the hens nest, then break the baby
                # generation function.
                if (len(self.hens) > r * hensImpregnatedPerRooster):
                    # self.roosters[r].bred = 1               # Mark rooster as bred. If a hen or rooster
                                                            # has bred in a cycle, it will not attempt to
                                                            # cross the road
                    self.roosters[r].aggression += 0.01     # Breeding makes roosters more aggressive
                    
                    # Get the hen list starting index and ending index based on the number of hens
                    # a rooster can impregnate in a single cycle.
                    for h in range(r * hensImpregnatedPerRooster, r * hensImpregnatedPerRooster + hensImpregnatedPerRooster):
                        # While we haven't exceeded the number of hens, we'll continue to breed them.
                        # If the list ends in the middle of a breeding spree, break egg train
                        if h < len(self.hens):
                            # self.hens[h].bred = 1           # Mark hen as bred.                                                             # 
                            self.hens[h].aggression += 0.005# Increase aggression
                            
                            # As population control, I've given a maximum fertility age to hens. While
                            # they can no longer create chickens, these cougars can still take up valuable
                            # breeding slots
                            if self.hens[h].age <= henFertileAge and random.random() < chanceFertilizedEgg:
                                # Generate a new chicken. It's total aggression is the average of the parents
                                # as well as the average of their parents speed. This makes the offspring more
                                # fit for breeding and survival.
                                newChicken = Chicken(
                                    (self.hens[h].aggression + self.roosters[r].aggression)/2 
                                    , (self.hens[h].speed + self.roosters[r].speed)/2 
                                    )
                                newRoosters.append(newChicken) if random.random() < maleChance else newHens.append(newChicken)
                        else:
                            break
                else:
                    break
            
            # Determine whose crossing the roads. These unbred chickens/roosters have a chance to find a new place
            # place to live where they can can breed. Crossing a road successfully increases a chickens speed,
            # increasing its fitness for breeding. If there are more roosters than needed for a breeding cycle,
            # we run the roosters
            # Reduce the number of times we have to transmit go through array. Need formula to find the last next
            # rooster to breed.
            # Roosters 10 Hens 21, 2 hens per one rooster. Easier check. 
            # 10 * 2 the == 20... maximum number of hens hens from index 20 onwards are moveable.
            # Roosters 20, Hens 21, 2 hens per rooster. In this case, 11 roosters can breed, so ceiling(21/2)            
            if len(self.hens) > len(self.roosters) * hensImpregnatedPerRooster:
                # Hen run!
                self.whyDidTheChickenCrossTheRoad(
                    len(self.roosters) * hensImpregnatedPerRooster
                    , "female"
                )
            else:
                # Rooster run!
                self.whyDidTheChickenCrossTheRoad(
                    math.ceil(len(self.hens)/hensImpregnatedPerRooster)
                    , "male"
                )

            # Age the birds
            for r in self.roosters:
                r.age += 1
            for h in self.hens:
                h.age += 1

            # Increase the populations based on breeding results
            self.roosters += newRoosters
            self.hens     += newHens

            # Print the population statistics
            roosterArr.append(len(self.roosters))
            henArr.append(len(self.hens))
            totalArr.append(len(self.roosters) +len(self.hens))

        x = list(range(0, cycles + 1))
        plt.plot(x, roosterArr, label = "Roosters")
        plt.plot(x, henArr, label = "Hens")
        plt.plot(x, totalArr, label = "Total")
        plt.legend()

        plt.show()
        # input("Hit ENTER to continue!")
   

if __name__ == "__main__":
    nest = Nest("BBQ", 20)
    nest.createRoad("KFC", 0.20)
    nest.createRoad("Popeye's", 0.40)
    nest.createRoad("Wendy's", 0.30)
    nest.simulateNest(cycles)
    # input("Hit ENTER to quit!")



'''
chickens = 20
breed = 0.125
cross = 0.10
death = 0.50

chArr = [chickens]
bArr  = [0]
crArr = [0]
dArr  = [0]

def simulation(cycles):
    global chickens
    global chArr    
    global bArr
    global crArr
    global dArr
    
    # Nest logic
    for i in range(1, cycles + 1):
        c = chickens
        bred = 0
        crossed = 0
        died = 0
        for ch in range(c):
            if (random.random() < breed):
                chickens = chickens + 1
                bred = bred + 1
            elif random.random() < cross:
                crossed = crossed + 1
                if random.random() < death:
                    chickens = chickens - 1
                    died = died + 1
        print(f'Cycle {i}: {chickens} chickens | {bred} bred | {crossed} crossed | {died} died')
        chArr.append(chickens)
        bArr.append(bred)
        crArr.append(crossed)
        dArr.append(died)

simulation(50)
x = list(range(0, 51))

plt.plot(x, chArr, label="Chickens")
plt.plot(x, bArr, label="Bred")
plt.plot(x, crArr, label="Crossed")
plt.plot(x, dArr, label="Died")
plt.legend()
plt.yticks(np.arange(0, chickens + (100-(chickens%100)), 50))
plt.show()
'''