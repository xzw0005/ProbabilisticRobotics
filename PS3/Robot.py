'''
Created on May 27, 2017

@author: Xing Wang
'''

import math
import random

landmarks = [[20., 20.], [80., 80.], [20., 80.], [80., 20.]]
world_size = 100.

class robot(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.x = random.random() * world_size
        self.y = random.random() * world_size
        self.orientation = random.random() * 2. * math.pi
        self.forword_noise = 0.
        self.turn_noise = 0. 
        self.sense_noise = 0. 
        
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError('X coordinate out of bound')
        if new_y < 0 or new_y >= world_size:
            raise ValueError('Y coordinate out of bound')
        if new_orientation < 0 or new_orientation >= 2*math.pi:
            raise ValueError('Orientation must be in [0, 2pi)')
        self.x = new_x
        self.y = new_y
        self.orientation = new_orientation
        
    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # Makes it possible to change the noise parameters 
        # This is often useful in particle filters 
        self.forword_noise = float(new_f_noise)
        self.turn_noise = float(new_t_noise)
        self.sense_noise = float(new_s_noise)
        
    def sense(self):
        z = []
        for i in range(len(landmarks)):
            dist = math.sqrt((self.x - landmarks[i][0])**2 + (self.y - landmarks[i][1])**2)
            dist += random.gauss(0., self.sense_noise)
            z.append(dist)
        return z
    
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError('Robot cannot move backwards')
        # Turn, and add randomness to the turning command 
        orientation = self.orientation + float(turn) + random.gauss(0., self.turn_noise)
        orientation %= 2*math.pi 
        # Move, and add randomness to the motion command 
        dist = float(forward) + random.gauss(0., self.forword_noise)
        x = self.x + math.cos(orientation) * dist
        y = self.y + math.sin(orientation) * dist 
        x %= world_size     # Cyclic Truncate 
        y %= world_size
        # Set particle 
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forword_noise, self.turn_noise, self.sense_noise)
        return res 
    
    def Gaussian(self, mu, sigma, x):
        # Compute 1-dim Gaussian pdf
        return math.exp(-0.5 * (x-mu)**2 / (sigma**2)) / math.sqrt(2. * math.pi * sigma**2)
    
    def measurement_prob(self, measurement):
        # Calculate how likely a measurement should be
        prob = 1.
        for i in range(len(landmarks)):
            dist = math.sqrt((self.x - landmarks[i][0])**2 + (self.y - landmarks[i][1])**2) 
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob 
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))
    
