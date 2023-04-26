import random
import matplotlib.pyplot as plt
import numpy as np

maleChance = 0.50
startingAggression = 0.10
startingSpeed = 0.10
startingPop = 10

class Chicken():
    def __init__(self, agg, spd) -> None:
        self.gender = 1 if random.random() < maleChance else 0  # 1: male  2: female
        self.aggression = agg   # Aggression level
        self.speed = spd        # Speed
        self.age = 0            # Age
        self.bred = 0           # Boolean, whether they bred this cycle or not

class Nest():
    def __init__(self, startingPop = 0):
        self.cocks = []         # Male chicken array
        self.hens  = []         # Female chicken array
        self.roads = []         # List of adjacent nests and the danger of crossing the road

    def createRoad(self, name, danger): # Create a road and append to the roads list
        self.roads.append({
            "name": name                # Name of the adjacent nest
            , "danger": danger          # Danger of crossing the road
        })


    def simulateNest(self, cycles):
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