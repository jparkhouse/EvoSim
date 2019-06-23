#File to add code for the environment in which the creatures reside
import Creatures as crt
import numpy as np
import copy as copy
import math as maths

def generateRandomNumberWithLowerLimit (mean, sigma, lower_limit):
    '''
    Generates a random number based on a gaussian destribution, adding a lower limit to what that number can be
    '''
    x = np.random.normal(mean, sigma)

    while (x < lower_limit):
        x = np.random.normal(mean, sigma)
    return x


def generateFoodVariables (length_of_map, mean_energy = 400.0):
    '''
    Takes the length of the map from side to side and generates a random position, with higher chance of it being near the centre
    '''

    x = np.random.normal(0.0, 15)
    while (abs(x) > length_of_map/2):
        x = np.random.normal(0.0, 15)
    y = np.random.normal(0.0, 15)
    while (abs(y) > length_of_map/2):
        y = np.random.normal(0.0, 15)
    energy = generateRandomNumberWithLowerLimit (mean_energy, 0.2, 0.01)

    return x,y,energy

def generateCreatureVariables (length_of_map, mean_speed = 1.0, mean_radius = 1.0, mean_sensory_range = 40, baby = False):
    '''
    Takes the length of the map from side to side and generates all the random variables needed for a creature to work. the result cannot be passed directly to the creature init function since it lacks environment
    '''
    #chooses a random part of the borders to spawn the creatures in
    if not baby:
        border = np.random.choice([1, 2, 3, 4])  
        if (1 == border):
            y = -50
            x = np.random.normal(0.0, 15)
            while (abs(x) > length_of_map/2):
                x = np.random.normal(0.0, 15)
        elif (2 == border):
            x = -50
            y = np.random.normal(0.0, 15)
            while (abs(y) > length_of_map/2):
                y = np.random.normal(0.0, 15)
        elif (3 == border):
            y = 50
            x = np.random.normal(0.0, 15)
            while (abs(x) > length_of_map/2):
                x = np.random.normal(0.0, 15)
        elif (4 == border):
            x = 50
            y = np.random.normal(0.0, 15)
            while (abs(y) > length_of_map/2):
                y = np.random.normal(0.0, 15)

    if baby:
        standard_deviation = 0.05
    else:
        standard_deviation = 0.2

    speed         = generateRandomNumberWithLowerLimit (mean_speed, 0.3, standard_deviation)
    radius        = generateRandomNumberWithLowerLimit (mean_radius, 0.3, standard_deviation)
    sensory_range = generateRandomNumberWithLowerLimit (mean_sensory_range, 5, standard_deviation)
    if baby:
        return speed, radius, sensory_range
    else:
        return  x, y, speed, radius, sensory_range

def getDistance(position_one, position_two):
    '''
    Takes in two touples of (x,y) locations and finds the distance between them
    '''
    return pow((pow((position_one[0]-position_two[0]),2) + pow((position_one[1]-position_two[1]),2)),1/2)


class Environment(object):
    def __init__(self, number_of_creatures, number_of_foods, tick_length = 1, number_of_ticks = 100):

        '''
        Defines the enviroment on the class calling
        '''

        creatures = []
        for i in range (number_of_creatures):
            x, y, speed, radius, sensory_range = generateCreatureVariables (100)
            creatures.append(crt.Creature(x, y, speed, 500, radius, sensory_range, self))
        self.creatures = creatures
        
        #will get the position and size of each creature
        positions_of_creatures = []
        radii_of_creatures     = []
        for i in range (len(creatures)):
            positions_of_creatures.append(creatures[i].getLocation())
            radii_of_creatures    .append(creatures[i].radius)
        self.positions_of_creatures = positions_of_creatures
        self.radii_of_creatures     = radii_of_creatures

        self.generateNewFoods(number_of_foods)
        
        self.radii_of_creatures_over_time = [copy.deepcopy(self.radii_of_creatures)]
        self.radii_of_foods_over_time     = [copy.deepcopy(self.radii_of_foods)]

        self.creature_positions_over_time = [copy.deepcopy(self.positions_of_creatures)]
        self.food_positions_over_time     = [copy.deepcopy(self.positions_of_foods)]  
        
        self.averages_over_cycles = [self.getAverages()]

        #####Define tick_length, to change when we know more about it#####
        self.tick_length = tick_length
        self.number_of_ticks = number_of_ticks
        self.number_of_foods = number_of_foods
        self.current_tick = 0

    def generateNewFoods (self, number_of_foods):
        '''
        adds a set of new foods to the board
        '''
        foods = []
        for i in range (number_of_foods):
            food_x_location, food_y_location, food_energy = generateFoodVariables (100)
            foods.append(Food(food_x_location, food_y_location, food_energy))
        self.foods = foods

        positions_of_foods = []
        radii_of_foods     = []
        for i in range (len(foods)):
            positions_of_foods.append(foods[i].getLocation())
            radii_of_foods    .append(foods[i].radius)
        self.positions_of_foods = positions_of_foods
        self.radii_of_foods     = radii_of_foods

    def getObjects(self):

        '''
        returns the coordinates of the piece of food
        '''
        all_objects = []
        for i in range (len(self.creatures)):
            temp = []
            temp.extend([self.creatures[i],self.creatures[i].getLocation()])
            all_objects.append(temp)  
        for i in range (len(self.foods)):
            temp = []
            temp.extend([self.foods[i],self.foods[i].getLocation()])
            all_objects.append(temp)   
        return (all_objects)

    def tick (self):
        
        '''
        Makes a time unit pass in the simulation
        '''
        #goes through each of the creatures
        for i in range (len(self.creatures)):
            #gets the direction it will move in
            direction = self.creatures[i].findPath(self.tick_length)
            #makes the creature move in that direction
            self.creatures[i].moveOneTick(direction,self.tick_length)
            # updates the list of positions
            self.positions_of_creatures[i] = self.creatures[i].getLocation()
            #checks if the creature ovelaps with food, and if so, consumes it and then removes it from the list of foods
            foods_eaten = []
            for j in range (len(self.foods)):
                distance = getDistance(self.positions_of_foods[j],self.positions_of_creatures[i])
                if (distance < (self.creatures[i].radius+self.foods[j].radius)):
                    self.creatures[i].eatFood(self.foods[j].energy)
                    foods_eaten.append(j)
            for k in range (len(foods_eaten)):
                #deletes the foods that were eaten(the -k is there so that after the first food is deleted, the next one deleted is not affected by the change in numbering in the whole thing
                del self.foods[foods_eaten[k]-k]
                del self.positions_of_foods[foods_eaten[k]-k]
                del self.radii_of_foods[foods_eaten[k]-k]


        radii_of_foods= []
        for i in range (len(self.foods)):
            radii_of_foods.append(self.foods[i].radius)
        self.radii_of_foods= radii_of_foods

        radii_of_creatures= []
        for i in range (len(self.creatures)):
            radii_of_creatures.append(self.creatures[i].radius)
        self.radii_of_creatures= radii_of_creatures
        
        self.radii_of_creatures_over_time.append(copy.deepcopy(self.radii_of_creatures))
        self.creature_positions_over_time.append(copy.deepcopy(self.positions_of_creatures))

        self.food_positions_over_time    .append(copy.deepcopy(self.positions_of_foods))
        self.radii_of_foods_over_time    .append(copy.deepcopy(self.radii_of_foods))

        self.current_tick += 1
        pass

    def getAnimationData (self):
        '''
        returns 4 lists, one that contains all the lists of creatures after each tick, one all the lists of creature positions after each tick, one all the lists of food after each tick, and one all the lists of food positions over each tick
        '''
        return (self.radii_of_creatures_over_time, self.creature_positions_over_time, self.radii_of_foods_over_time, self.food_positions_over_time)

    def runCycle(self):
        '''
        cicles through the specified number of ticks and returns the animation data
        '''
        for i in range (self.number_of_ticks):
            self.tick()
            print("{0}th tick done. {1}% complete".format(i,int((i/self.number_of_ticks)*100)))
        return (self.getAnimationData())

    def afterCycle (self):
        '''
        alters everything that needs to be altered in the environment in between cycles
        '''
        #generate new foods
        self.generateNewFoods(self.number_of_foods)
        self.current_tick = 0
        creatures_to_split = []
        #cycle through all creatures
        i = 0
        for i in range(len(self.creatures)):
            if (48 > abs(self.creatures[i].x_location)) and (48 > abs(self.creatures[i].y_location)):
                #do something to simulate not safeness
                self.creatures[i].current_energy += -400/self.radii_of_creatures[i]
        i = 0
        while (i<(len(self.creatures))):
            if (0 >= self.creatures[i].current_energy):
                #remove ones with not that much
                del self.creatures[i]
                del self.positions_of_creatures[i]
                del self.radii_of_creatures[i]
            else:
                i += 1
        new_creatures = []
        for i in range(len(self.creatures)):
            reproduction_chance = 200*maths.atan(self.creatures[i].current_energy/800)/maths.pi
            if np.random.uniform(0,100) <= reproduction_chance:
                #makesomebabies.exe in new list
                for j in range (2):
                    speed, radius, sensory_range = generateCreatureVariables (100, mean_speed = self.creatures[i].speed, mean_radius = self.creatures[i].radius, mean_sensory_range = self.creatures[i].sensory_range, baby = True)
                    new_creatures.append(crt.Creature(self.creatures[i].x_location+2*pow(-1,j), self.creatures[i].y_location+2*pow(-1,j), speed, self.creatures[i].current_energy/2, radius, sensory_range, self))
                #mark creatures
                creatures_to_split.append(i)
        
        for i in range(len(creatures_to_split)):
            del self.creatures[creatures_to_split[i]-i]
            del self.positions_of_creatures[creatures_to_split[i]-i]
            del self.radii_of_creatures[creatures_to_split[i]-i]
            pass
        #old list extend new list
        for i in range (len(new_creatures)):
            self.positions_of_creatures.append(new_creatures[i].getLocation())
            self.radii_of_creatures    .append(new_creatures[i].radius)

        self.creatures.extend(new_creatures)

        self.radii_of_creatures_over_time = [copy.deepcopy(self.radii_of_creatures)]
        self.radii_of_foods_over_time     = [copy.deepcopy(self.radii_of_foods)]
        self.creature_positions_over_time = [copy.deepcopy(self.positions_of_creatures)]
        self.food_positions_over_time     = [copy.deepcopy(self.positions_of_foods)] 

        self.averages_over_cycles.append(self.getAverages())
    
    def  getAverages (self):
        '''
        returns the average speed, radius, and sensory range of all creatures curently in the environment, as well as the current number of creatures alive
        '''
        sum_of_creature_speeds         = 0
        sum_of_creature_radii          = 0
        sum_of_creature_sensory_ranges = 0
        
        for i in range (len(self.creatures)):
            sum_of_creature_speeds         += self.creatures[i].speed
            sum_of_creature_radii          += self.creatures[i].radius
            sum_of_creature_sensory_ranges += self.creatures[i].sensory_range
        
        if 0 != len(self.creatures):
            average_speed         = sum_of_creature_speeds        /len(self.creatures)
            average_radius        = sum_of_creature_radii         /len(self.creatures)
            average_sensory_range = sum_of_creature_sensory_ranges/len(self.creatures)
        else:
            average_speed         = 0
            average_radius        = 0
            average_sensory_range = 0          


        return average_speed,average_radius,average_sensory_range, len(self.creatures)


class Food(object):
    def __init__(self, x_location, y_location, energy):

        '''
        Defines a piece of food on the class calling
        '''

        self.energy     = energy
        self.x_location = x_location
        self.y_location = y_location
        self.radius     = 4*pow((energy/420000),(1/3))


    def getLocation(self):

        '''
        returns the coordinates of the piece of food
        '''

        return (self.x_location, self.y_location)
    pass



  