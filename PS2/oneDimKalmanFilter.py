'''
Created on May 25, 2017

@author: Xing Wang
'''

def update(mean1, var1, mean2, var2):
    # measurement step
    new_mean = (var2 * mean1 + var1 * mean2) * 1. / (var1 + var2)
    new_var = 1 / (1. / var1 + 1. / var2)
    return [new_mean, new_var]

def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]
    
measurements =  [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4
motion_sig = 2

mu = 0
sig = 1e-10

for k in range(len(measurements)):
    z = measurements[k]
    [mu, sig] = update(mu, sig, z, measurement_sig)
    print 'update: ', mu, sig
    u = motion[k]
    [mu, sig] = predict(mu, sig, u, motion_sig)
    print 'predict: ', mu, sig
