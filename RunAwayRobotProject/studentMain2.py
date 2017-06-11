'''
Created on Jun 8, 2017

@author: Xing Wang
'''
# ----------
# Part Two
#
# Now we'll make the scenario a bit more realistic. Now Traxbot's
# sensor measurements are a bit noisy (though its motions are still
# completetly noise-free and it still moves in an almost-circle).
# You'll have to write a function that takes as input the next
# noisy (x, y) sensor measurement and outputs the best guess 
# for the robot's next position.
#
# ----------
# YOUR JOB
#
# Complete the function estimate_next_pos. You will be considered 
# correct if your estimate is within 0.01 stepsizes of Traxbot's next
# true position. 
#

from robot import *  # Check the robot.py tab to see how this works.
from math import *
from matrix import * # Check the matrix.py tab to see how this works.
import random

def mean(lists):
    sums = 0
    for i in range(len(lists)):
        sums += lists[i]
    return sums/len(lists)

def estimate_next_pos(measurement, OTHER = None):
    """Estimate the next (x, y) position of the wandering Traxbot
    based on noisy (x, y) measurements."""

    if not OTHER:
        OTHER = robot()        
        OTHER.distance_history = []
    distance_history = OTHER.distance_history
    dy = measurement[1] - OTHER.y
    dx = measurement[0] - OTHER.x
    beta = atan2(dy, dx)
    distance = distance_between(measurement, OTHER.sense())
    distance_history.append(distance)
    mean_distance = sum(distance_history) * 1.0 / len(distance_history)
    turning = beta - OTHER.heading
    heading = beta + turning
    xp = measurement[0] + mean_distance * cos(heading)
    yp = measurement[1] + mean_distance * sin(heading)
    OTHER = robot(measurement[0], measurement[1], beta)
    OTHER.distance_history = distance_history
    xy_estimate = (xp, yp)
    return xy_estimate, OTHER

#this calculates the angle between 2 points using the law of cosines
def angle_between(p1, p2):
    x1,y1 = p1[0],p1[1]
    x2,y2 = p2[0],p2[1]
    return acos((x1*x2 + y1*y2) / (sqrt(x1**2 + y1**2) * sqrt(x2**2 + y2**2)))

# A helper function you may find useful.
def distance_between(point1, point2):
    """Computes distance between point1 and point2. Points are (x, y) pairs."""
    x1, y1 = point1
    x2, y2 = point2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# This is here to give you a sense for how we will be running and grading
# your code. Note that the OTHER variable allows you to store any 
# information that you want. 
def demo_grading(estimate_next_pos_fcn, target_bot, OTHER = None):
    localized = False
    distance_tolerance = 0.01 * target_bot.distance
    ctr = 0
    # if you haven't localized the target bot, make a guess about the next
    # position, then we move the bot and compare your guess to the true
    # next position. When you are close enough, we stop checking.
    while not localized and ctr <= 1000:
        ctr += 1
        measurement = target_bot.sense()
        position_guess, OTHER = estimate_next_pos_fcn(measurement, OTHER)
        target_bot.move_in_circle()
        true_position = (target_bot.x, target_bot.y)
        error = distance_between(position_guess, true_position)
        if error <= distance_tolerance:
#             print "You got it right! It took you ", ctr, " steps to localize."
            localized = True
#         if ctr == 1000:
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
test_target = robot(2.1, 4.3, 0.5, 2*pi / 34.0, 1.5)
measurement_noise = 0.05 * test_target.distance
test_target.set_noise(0.0, 0.0, measurement_noise)

# demo_grading(estimate_next_pos, test_target)

# succ = 0
# for i in range(1000):
#     succ += demo_grading(estimate_next_pos, test_target)
# print succ


