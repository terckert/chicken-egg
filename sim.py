import random
import matplotlib.pyplot as plt
import numpy as np

maleChance = 0.60
chanceOfMovingIfNotBred = 0.0
chanceFertilizedEgg = 0.60
startingAggression = 0.10
startingSpeed = 0.10
startingPop = 10
maxAge = 7
henFertileAge = 3
hensImpregnatedPerRooster = 3

# Fitness stats. Speed and aggression factor into a roosters chance to breed. The more
# fit a rooster is to breed, the more likely they will find mates. These are the controls
# where we can weight speed or aggression. 1 one indicates that the entire stat is factored
# into fitness, while a 2 will weight it at half its value.
speedWeight = 1
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
        
        self.roosters = []         # Male chicken array
        self.hens  = []         # Female chicken array
        self.roads = []         # List of adjacent nests and the danger of crossing the road
        
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
            self.roosters = sorted(self.roosters, key= lambda r: (r.aggression*aggressionWeight) + (r.speed*speedWeight))
            random.shuffle(self.hens)

            # Clear the list of next gen chickens
            newRoosters = []
            newHens = []

            # Clear the breeding variables
            for r in self.roosters:
                r.bred = 0
            for h in self.hens:
                h.bred = 0
            # Breed them. 
            for r in range(len(self.roosters)):
                # Check if enough hens exits to the rooster to breed with. If the length of the 
                # hens list is greater than rooster index * the number of hens the rooster can breed
                # with, we get our breed on. If we've exceeded the hens nest, then break the baby
                # generation function.
                if (len(self.hens) > r * hensImpregnatedPerRooster):
                    self.roosters[r].bred = 1               # Mark rooster as bred. If a hen or rooster
                                                            # has bred in a cycle, it will not attempt to
                                                            # cross the road
                    self.roosters[r].aggression += 0.01     # Breeding makes roosters more aggressive
                    
                    # Get the hen list starting index and ending index based on the number of hens
                    # a rooster can impregnate in a single cycle.
                    for h in range(r * hensImpregnatedPerRooster, r * hensImpregnatedPerRooster + hensImpregnatedPerRooster):
                        # While we haven't exceeded the number of hens, we'll continue to breed them.
                        # If the list ends in the middle of a breeding spree, break egg train
                        if h < len(self.hens):
                            self.hens[h].bred = 1           # Mark hen as bred.                                                             # 
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
            if len(self.hens) <= len(self.roosters) * hensImpregnatedPerRooster + hensImpregnatedPerRooster:
                for r in self.roosters:
                    if r.bred == 0:
                        if random.random() < chanceOfMovingIfNotBred: # Chance of dying, TODO: integrate neighbors list
                            if random.random() < 0.50 - r.speed:
                                r.alive = 0
                            else: # Increase the speed of survivors to be passed on to the next generations
                                r.speed += .01
                # Remove the dead
                self.roosters = [r for r in self.roosters if r.alive == 1]
            else:
                for h in self.hens:
                    if h.bred == 0:
                        if random.random() < chanceOfMovingIfNotBred: # Chance of dying, TODO: integrate neighbors list
                            if random.random() < 0.50 - h.speed:
                                h.alive = 0
                            else: # Increase the speed of survivors to be passed on to the next generations
                                h.speed += .01
                # Remove the dead.
                self.hens  = [h for h in self.hens if h.alive == 1]

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
    nest.simulateNest(100)
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