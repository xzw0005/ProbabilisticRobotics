'''
Created on May 23, 2017

@author: XING
'''
import PS2.matrix as matrix

# if __name__ == '__main__':
measurements = [1, 2, 3]

x = matrix.matrix([[0.], [0.]]) # initial state (location and velocity)
P = matrix.matrix([[1000., 0.], [0., 1000.]]) # initial uncertainty covariance
u = matrix.matrix([[0.], [0.]]) # external motion
F = matrix.matrix([[1., 1.], [0, 1.]]) # next state function
H = matrix.matrix([[1., 0.]]) # measurement function
R = matrix.matrix([[1.]]) # measurement uncertainty (i.e., noise)
I = matrix.matrix([[1., 0.], [0., 1.]]) # identity matrix

def kalman_filter(x, P):
    for k in range(len(measurements)):
        z = matrix.matrix([[measurements[k]]])
        x, P = predict(z, x, P)
        x, P = update(x, P)       
        print 'x= '
        x.show()
        print 'P= '
        P.show()
    return x, P

def update(x, P):
    x = F * x + u
    P = F * P * F.transpose()
    return x, P

def predict(z, x, P):
    y = z - H * x       # Error
    S = H * P * H.transpose() + R
    K = P * H.transpose() * S.inverse()
    x= x + K * y 
    P = (I - K * H) * P
    return x, P

print kalman_filter(x, P)
