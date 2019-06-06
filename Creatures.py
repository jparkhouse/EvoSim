#File to add code for the creatures
import math
import Environment as env
import numpy as np

unique_ID = 0

class Creature(object):

    '''
    The class to define a creature, its properties and the various things it can do
    '''

    def __init__(self, x_location, y_location, speed, starting_energy, radius, sensory_range, environment):

        '''
        Defines a creature on the class calling
        '''

        self.x_location = x_location
        self.y_location = y_location
        self.speed = speed
        self.current_energy = starting_energy
        self.radius = radius
        self.volume = 4/3 * math.pi * pow(self.radius,3)
        self.sensory_range = sensory_range
        self.environment = environment

        global unique_ID
        unique_ID += 1
        self.ID = unique_ID #possibly not needed?

    def moveOneTick(self,direction,tick_length):

        '''
        Moves the creature for a distance defined by 'self.speed' * 'tick_length' in direction 'direction', a radian value from the positive x axis in a counter-clockwise direction (as is the standard in maths), then subtracts the distance moved from energy required to make this manuever from the current energy
        '''

        self.x_location += (self.speed * tick_length * math.cos(direction))
        self.y_location += (self.speed * tick_length * math.sin(direction))
        self.current_energy += -(self.volume * self.speed / tick_length) # based off of mv^2/2 - except wanted it to be per unit distance, so then divide by distance, which becomes mv^2/2*v*t, which is mv/2t. Very much up to debate.

    def eatFood(self, food_energy):
        
        '''
        Adds food consumed to the current energy
        '''

        self.current_energy += food_energy

    def getSensoryData(self):
        
        '''
        Discovers what is within the sensory range of the creature
        '''

        all_objects = self.environment.getObjects()
        relevant_objects = []
        for each in all_objects:
            if self.x_location - self.sensory_range <= each[1][0] <= self.x_location + self.sensory_range: #rules out by x
                if self.y_location - self.sensory_range <= each[1][1] <= self.y_location + self.sensory_range: #rules out by y
                    if pow(pow(self.y_location - each[1][1], 2) + pow(self.x_location - each[1][0], 2), 1/2) <= self.sensory_range: # actually calculates the distance
                        relevant_objects.append([each[0], each[1], env.getDistance(self.getLocation(),each[0].getLocation())])
        relevant_objects.sort(key = lambda x:x[2]) #sorts by distance to object
        return relevant_objects
        

    def findPath(self):

        '''
        Method in charge of finding the best path for the creature. returns a direction in which to travel
        '''

        i = 0
        relevant_objects = self.getSensoryData()
        try:
            while not isinstance(relevant_objects[i][0],env.Food): #ticks through until the first peice of food is found
                i += 1
        except:
            a = np.random.random() - 0.5 #pick a random x between -0.5 and 0.5
            b = np.random.random() - 0.5 #pick a random y between -0.5 and 0.5
            while not (-50 <= (self.speed * tick_length * math.cos(getDirection((a,b)))+ self.x_location) <= 50 
                       and -50 <= (self.speed * tick_length * math.sin(getDirection((a,b)))+ self.y_location) <= 50): #checks to make sure that moving in this direction wont move it outside the environment arena, if it does, reselect a and b
                a = np.random.random() - 0.5
                b = np.random.random() - 0.5
            return getDirection((a,b)) #return this random direction
        return getDirection((relevant_objects[i][1][0]-self.x_location,relevant_objects[i][1][1]-self.y_location))
        

    def getLocation(self):

        '''
        returns the coordinates of the creature
        '''

        return (self.x_location, self.y_location)

    def runTick(self,tick_length):
        
        '''
        defines how the creature deals with a tick
        '''

        self.current_energy += -(0.007*self.sensory_range*self.volume)

def getDirection(vec):
    return math.acos(vec[0]/pow(pow(vec[0],2) + pow(vec[1],2),1/2))
