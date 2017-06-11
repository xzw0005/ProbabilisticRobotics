'''
Created on Jun 7, 2017

@author: Xing Wang
'''
from robot import *
from matrix import *
from math import *
import random

def estimate_next_pos(measurement, OTHER=None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""
    # TODO
#     if not OTHER:
#         OTHER = robot()
#     distance = distance_between(measurement, OTHER.sense())
#     x, y = measurement
#     dy = y - OTHER.y
#     dx = x - OTHER.x
#     last_heading = OTHER.heading
#     beta = atan2(dy, dx)
#     OTHER.heading = beta
#     turning = beta - last_heading
#     OTHER.move(turning, distance)   
#     xy_estimate = OTHER.sense()
#     OTHER = robot(measurement[0], measurement[1], beta)
#     return xy_estimate, OTHER
        
    if not OTHER:
        OTHER = robot()        
    dy = measurement[1] - OTHER.y
    dx = measurement[0] - OTHER.x
    beta = atan2(dy, dx)
    distance = distance_between(measurement, OTHER.sense())
    turning = beta - OTHER.heading
    heading = beta + turning
    xp = measurement[0] + distance * cos(heading)
    yp = measurement[1] + distance * sin(heading)
    OTHER = robot(measurement[0], measurement[1], beta)
    xy_estimate = (xp, yp)
    return xy_estimate, OTHER

def distance_between(point1, point2):
    x1, y1 = point1
    x2, y2 = point2 
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)   

def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    while not localized and ctr <= 10: 
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
            localized = True
#             print "You got it right! It took you ", ctr, " steps to localize."
#         if ctr == 10:
#             print "Sorry, it took you too many steps to localize the target."
    return localized

# This is a demo for what a strategy could look like. This one isn't very good.
def naive_next_pos(measurement, OTHER = None):
    """This strategy records the first reported position of the target and
    assumes that eventually the target bot will eventually return to that 
    position, so it always guesses that the first position will be the next."""
    if not OTHER: # this is the first measurement
        OTHER = measurement
    xy_estimate = OTHER 
    return xy_estimate, OTHER

# This is how we create a target bot. Check the robot.py file to understand
# How the robot class behaves.

# test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
# test_target.set_noise(0.0, 0.0, 0.0)
# 
# # demo_grading(estimate_next_pos, test_target)
# 
# succ = 0
# for i in range(1000):
#     succ += demo_grading(estimate_next_pos, test_target)
# print succ