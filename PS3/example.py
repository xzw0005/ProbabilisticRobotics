'''
Created on May 27, 2017

@author: Xing Wang
'''

import PS3.Robot as Robot
import random

myrobot = Robot.robot()
myrobot = myrobot.move(0.1, 5.0)
z = myrobot.sense()

N = 1000
##### Initialization #####
p = []
for i in range(N):
    r = Robot.robot()
    r.set_noise(0.05, 0.05, 5.0)
    p.append(r)

T = 10
for t in range(T):
    myrobot = myrobot.move(0.1, 5.0)
    z = myrobot.sense()
    
    p2 = []
    for i in range(N):
        p2.append(p[i].move(0.1, 5.0))
    p = p2
    
    w = []
    for i in range(N):
        w.append(p[i].measurement_prob(z))
    wmax = max(w)
    
    ######################
    # Resampling Wheel
    ######################
    p3 = []
    index = int(random.random() * N)
    beta = 0.0
    for j in range(N):
        beta += random.random() * wmax * 2.0
        while beta > w[index]:
            beta -= w[index]
            index = (index + 1)%N 
        p3.append(p[index])
    p = p3
print p3