'''
Created on Jun 7, 2017

@author: Xing Wang
'''

import math
import random

# helper function to map all angles onto [-pi, pi]
def angle_trunc(a):
    while a < 0.0:
        a += math.pi * 2
    return ((a+math.pi)%(math.pi*2))-math.pi

class robot(object):
    '''
    classdocs
    '''


    def __init__(self, x=0., y=0., heading=0., turning=2*math.pi/10, distance=1.):
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        self.heading = heading
        self.turning = turning
        self.distance = distance
        self.turning_noise = 0. 
        self.distance_noise = 0. 
        self.measurement_noise = 0. 
        
    def set_noise(self, new_t_noise, new_d_noise, new_m_noise):
        self.turning_noise = float(new_t_noise)
        self.distance_noise = float(new_d_noise)
        self.measurement_noise = float(new_m_noise)
        
    def move(self, turning, distance, tolerance=1e-3, max_turning_angle=math.pi):
        turning = random.gauss(turning, self.turning_noise)
        distance = random.gauss(distance, self.distance_noise)
        
        # Truncate to fit physical limitation
        turning = max(-max_turning_angle, turning)
        turning = min(max_turning_angle, turning)
        distance = max(0., distance)
        
        # Execute Motion 
        self.heading += turning
        self.heading = angle_trunc(self.heading)
        self.x += distance * math.cos(self.heading)
        self.y += distance * math.sin(self.heading)
        
    def move_in_circle(self):
        self.move(self.turning, self.distance)
        
    def sense(self):
        x = random.gauss(self.x, self.measurement_noise)
        y = random.gauss(self.y, self.measurement_noise)
        return (x, y)
    
    def __repr__(self):
        return '[%.5f, %.5f]'%(self.x, self.y)