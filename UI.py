#File to add code for the display/UI
import Environment as env
import matplotlib.pyplot as plt
import math as maths
import numpy as np

#for the test, let's create 6 pieces of food and one creature
#radii_of_creatures_over_time, creature_positions_over_time, radii_of_foods_over_time, food_positions_over_time = env.runCycle(1, 6, 100)
def displayCycle(radii_of_creatures_over_time, creature_positions_over_time, radii_of_foods_over_time, food_positions_over_time,pause_time):
    fig, ax = plt.subplots()
    for i in range (99):
        #get the xs and the ys
        ax.cla()
        plt.xlim(-50, 50)
        plt.ylim(-50, 50)
        ax.text(-45,-45, "tick "+str(i+1))

        creatures_x_positions = []
        creatures_y_positions = []
        creatures_map_size    = []
        creature_markers = []
        for j in range (len(radii_of_creatures_over_time[i])):
            ax.add_artist(plt.Circle((creature_positions_over_time[i][j][0], creature_positions_over_time[i][j][1]), radii_of_creatures_over_time[i][j], color='r'))


        foods_x_positions = []
        foods_y_positions = []
        foods_map_size    = []
        for j in range (len(radii_of_foods_over_time[i])):
            ax.add_artist(plt.Circle((food_positions_over_time[i][j][0], food_positions_over_time[i][j][1]), radii_of_foods_over_time[i][j], color='b'))

        plt.draw()
    
        plt.pause(pause_time)
    plt.show()
    pass

def displayAfterCycle(averages_over_cycles):
    #average_speed_over_time ,average_radius_over_time ,average_sensory_range_over_time, number_of_creatures_over_time
    average_speed_over_time         =[]
    average_radius_over_time        =[]
    average_sensory_range_over_time =[]
    number_of_creatures_over_time   =[]
    for i in range(len(averages_over_cycles)):
        average_speed_over_time        .append(averages_over_cycles[i][0])
        average_radius_over_time       .append(averages_over_cycles[i][1])
        average_sensory_range_over_time.append(averages_over_cycles[i][2])
        number_of_creatures_over_time  .append(averages_over_cycles[i][3])

    cycles = range(len(average_speed_over_time))
    plt.clf()
    plt.figure(1)

    plt.subplot(221)
    plt.title('Average speed over cycles')
    plt.xlabel('cycle')
    plt.ylabel('Average speed')
    plt.bar(cycles, average_speed_over_time)

    plt.subplot(222)
    plt.title('Average radius over cycles')
    plt.xlabel('cycle')
    plt.ylabel('Average radius')
    plt.bar(cycles, average_radius_over_time)

    plt.subplot(223)
    plt.title('Average sensory range over cycles')
    plt.xlabel('cycle')
    plt.ylabel('Average sensory')
    plt.bar(cycles, average_sensory_range_over_time)

    plt.subplot(224)
    plt.title('Number of creatures over cycles')
    plt.xlabel('cycle')
    plt.ylabel('Number of creatures')
    plt.bar(cycles, number_of_creatures_over_time)
    
    plt.show()
    pass


    