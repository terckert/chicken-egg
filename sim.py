import random
import matplotlib.pyplot as plt
import numpy as np

maleChance = 0.50
startingAggression = 0.10
startingSpeed = 0.10
startingPop = 10
maxAge = 7
henFertileAge = 5

class Chicken():
    def __init__(self, agg, spd) -> None:
        self.aggression = agg   # Aggression level
        self.speed = spd        # Speed
        self.age = 0            # Age
        self.bred = 0           # Boolean, whether they bred this cycle or not

class Nest():
    def __init__(self, name, startingPop = 0):
        self.name  = name       # Name of the next
        
        self.cocks = []         # Male chicken array
        self.hens  = []         # Female chicken array
        self.roads = []         # List of adjacent nests and the danger of crossing the road
        
        global startingSpeed
        global startingAggression
        for i in range(startingPop):
            newChicken = Chicken(startingAggression, startingSpeed)
            self.cocks.append(newChicken) if random.random() < maleChance else self.hens.append(newChicken)

    def createRoad(self, name, danger): # Create a road and append to the roads list
        self.roads.append({
            "name": name                # Name of the adjacent nest
            , "danger": danger          # Danger of crossing the road
        })


    def simulateNest(self, cycles):
        cockArr  = [len(self.cocks)]
        henArr   = [len(self.hens)]
        totalArr = [len(self.cocks) +len(self.hens)]
        newCock  = []
        newHen   = [] 

        for i in range(1, cycles + 1):
            # Kill the old ones
            self.cocks = [c for c in self.cocks if c.age <= maxAge]
            self.hens  = [h for h in self.hens  if h.age <= maxAge]

            for i in self.cocks:
                i.bred = 0
            # Breed them. 
            for c in range(len(self.cocks)):
                if (len(self.hens) >= c*3):
                    self.cocks[c].bred = 1
                    self.cocks[c].aggression += 0.01                    
                    for h in range(c*3, c*3+3):
                        if h < len(self.hens):
                            self.hens[h].bred = 1
                            self.hens[h].aggression += 0.005
                            if self.hens[h].age <= henFertileAge:
                                newChicken = Chicken(
                                    (self.hens[h].aggression + self.cocks[c].aggression)/2 
                                    , (self.hens[h].speed + self.cocks[c].speed)/2 
                                    )
                                newCock.append(newChicken) if random.random() < maleChance else newHen.append(newChicken)
                        else:
                            break
                else:
                    break
        #     c = chickens
        #     bred = 0
        #     crossed = 0
        #     died = 0
        #     for ch in range(c):
        #         if (random.random() < breed):
        #             chickens = chickens + 1
        #             bred = bred + 1
        #         elif random.random() < cross:
        #             crossed = crossed + 1
        #             if random.random() < death:
        #                 chickens = chickens - 1
        #                 died = died + 1
        #     print(f'Cycle {i}: {chickens} chickens | {bred} bred | {crossed} crossed | {died} died')
            # chArr.append(chickens)
            # bArr.append(bred)
            # crArr.append(crossed)
            # dArr.append(died)        

if __name__ == "__main__":
    nest = Nest("BBQ", 20)
    nest.createRoad("KFC", 0.20)
    nest.simulateNest(10)
    input("Hit ENTER to quit!")



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