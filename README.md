# Chicken and Egg Simulation

Built as part of a special topic regarding internet scale systems design. This project was a fun competition that grew out of a discussion about build simulation and how important to simulate load when designing systems that had to scale to potentially millions of simulataneous users.

This project simulates the birth, breeding, and death of chickens. I coded a bunch of variables that could directly affect chickens or their environment in different ways and run it for so many cycles to see where we end up. It was added to a jupyter notebook for easy control and it provides cycle graphs that show general information about our chickens at the end.

## Simulation control variables
```{python}
# Number of cycles to run the simulation for
cycles = 100

# Knobs that can be turned on individual nests
"""##################################################################################################
Unused globals, whoops
##################################################################################################"""
startingPop                 = 10    # Starting population of a nest

"""##################################################################################################
Chicken generation levers, controls chicken base stats before lineage factored in
##################################################################################################"""
maleChance                  = 0.25  # Chance of male rooster hatching
startingSpeed               = 0.10  # Decreases the chance that a chicken will die crossing the
                                    # road
startingAggression          = 0.10  # Starting aggression rate, factors into fitness. At high 
                                    # aggression a chicken has a chance to kill another chicken

"""##################################################################################################
Breed levers, controls breeding levels and chicken murder
##################################################################################################"""
chanceOfMovingIfNotBred     = 0.50  # Chance that a chicken will leave the nest if it can't breed
chanceFertilizedEgg         = 0.50  # Chance that an egg will be fertilized in a cycle. Fertilized
                                    # eggs generate new pops
maxAge                      = 7     # Age at which chickens die of natural causes
henFertileAge               = 4     # Age at which hens stop producing eggs. They are still 
                                    # factored into breeding systems, but do not lay fertilized eggs
hensImpregnatedPerRooster   = 2     # Number of hens that a rooster can impregnate in a single cycle


"""##################################################################################################
Food levers, control your population through starvation. The Great Cluck Forwards!
##################################################################################################"""
startingFood                = 0.50  # Percentage of the maximum food that a nest starts with
foodGain                    = 1.00  # Percentage of the maximum food that a nest gets back at the
                                    # start of each cycle (after starvation checks and other stuff)
foodPerRooster              = 2     # Food consumed by roosters each cycle
foodPerHen                  = 1     # Food consumed by hens each cycle
roosterStarveModifier       = 0.50  # Modifies the chance a rooster will starve, chance * modifier
henStarveModifier           = 1.00  # Modifies the chance a hen will starve, chance * modifier
maxFoodIncrease             = 0.01  # The amount that a nest's maximum food is increased when
                                    # chickens don't eat all available food
maxFoodDecrease             = 0.10  # Percentage that a nest's maximum food is decreased when
                                    # chickens don't eat all available food
feastAggressionChange       = 0.005 # When there is enough food for all pops to eat, decrease a 
                                    # chickens aggression by this value due to a lack of competition.
                                    # This value should be positive. aggression + (value * -1)
famineAggressionChange      = 0.02  # When there is a food scarcity, increase aggression by this 
                                    # amount due to the competition for resources
                                    # This value should be positive, aggression + value

"""##################################################################################################
Fitness levers, determines rooster breeding order
##################################################################################################"""
speedWeight                 = 1.00  # Percentage of speed that is factored into breeding fitness
aggressionWeight            = 0.50  # Percentage of aggression that is factored into breeding
henBreedingAggression       = 0.005 # When a hen breeds, their aggression is increased by this amount
roosterBreedingAggression   = 0.01  # When a rooster breads, their aggression is increased by this
                                    # amount
speedForRoadCrossing        = 0.01  # When a chicken crosses the road, their speed is increased by
                                    # amount
murderousAggression         = 0.50  # Average aggression level at which a nest will suffer from
                                    # infighting. Infighting has a chance of killing off pops and
                                    # lowers the overall aggression of each surviving bird to a 
                                    # percentage of their current aggression.
postMurderAggression        = 0.25  # Percentage that a surviving chickens aggression level is
                                    # lowered to
baseChanceToDieInCombat     = 0.50  # Base chance that any given chicken will die from a war of
                                    # aggression. Formula for death chance is:
                                    # baseChance - (speed * speedWeight)

```
