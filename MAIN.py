#For running the code - acts like a .exe file

import Creatures as crt
import Environment as env
import UI

number_of_foods     = int(input("Please enter the number of foods generated per cycle "))
number_of_creatures = int(input("Please enter the number of creature the simulation starts with "))

environment = env.Environment(number_of_creatures, number_of_foods)
i = 0
while environment.creatures != []:
    i=i+1
    radii_of_creatures_over_time, creature_positions_over_time, radii_of_foods_over_time, food_positions_over_time = environment.runCycle()
    if 0 == i%10 or 1 == i:
        UI.displayCycle(radii_of_creatures_over_time, creature_positions_over_time, radii_of_foods_over_time, food_positions_over_time, 0.01)
    environment.afterCycle ()
    if 0 == i%10:
        UI.displayAfterCycle(environment.averages_over_cycles)