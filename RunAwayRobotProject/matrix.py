'''
Created on Jun 7, 2017

@author: Xing Wang
'''

from math import *
import random

class matrix(object):
    '''
    classdocs
    '''


    def __init__(self, value):
        '''
        Constructor
        '''
        self.value = value
        self.dimx = len(value)
        self.dimy = len(value[0])
        if value == [[]]:
            self.dimx = 0
            
    def zero(self, dimx, dimy):
        # check if valid dimensions
        if dimx < 1 or dimy < 1:
            raise ValueError("Invalid size of matrix")
        self.dimx = dimx
        self.dimy = dimy
        self.value = [[0 for row in range(dimy)] for col in range(dimx)]
        
    def identity(self, dim):
        # check if valid dimensions 
        if dim < 1:
            raise ValueError("Invalid size of matrix")
        self.dimx = dim 
        self.dimy = dim 
        self.value = [[0 for row in range(dim)] for col in range(dim)]
        for i in range(dim):
            self.value[i][i] = 1
            
    def show(self):
        for i in range(self.dimx):
            print self.value[i]
        print ' '
            
    def __add__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError("Matrices must be of equal dimension to add")
        res = matrix([[]])
        res.zero(self.dimx, self.dimy)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res.value[i][j] = self.value[i][j] + other.value[i][j]
        return res
    
    def __sub__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError("Matrices must be of equal dimensions to subtract")
        res = matrix([[]])
        res.zero(self.dimx, self.dimy)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res.value[i][j] = self.value[i][j] - other.value[i][j]
        return res
    
    def __mul__(self, other):
        # check if correct dimensions:
        if self.dimy != other.dimx:
            raise ValueError("Matrices must be mxn and nxp to multiply")
        res = matrix([[]])
        res.zero(self.dimx, self.dimy)
        for i in range(self.dimx):
            for j in range(self.dimy):
                for k in range(self.dimy):
                    res.value[i][j] += self.value[i][k] * other.value[k][j]
        return res
    
    def transpose(self):
        # compute transpose
        res = matrix([[]])
        res.zero(self.dimy, self.dimx)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res[j][i] = self.value[i][j]
        return res
    
    def Cholesky(self, ztol=1e-5):
        # compute the upper triangular Cholesky factorization of a positive definite matrix.
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)
        for i in range(self.dimx):
            temp = [res.value[k][i]**2 for k in range(i)]
            s = sum(temp)
            d = self.value[i][i] - s 
            if abs(d) < ztol:
                res.value[i][i] = 0. 
            else:
                if d < 0:
                    raise ValueError("Matrix is not positive-definite")
                res.value[i][i] = sqrt(d)
            for j in range(i+1, self.dimx):
                temp = [res.value[k][i] * res.value[k][j] for k in range(i)]
                s = sum(temp)
                if abs(s) < ztol:
                    s = 0. 
                res.value[i][j] = (self.value[i][j] - s) / res.value[i][i]
        return res
    
    def CholeskyInverse(self):
        # Compute inverse of matrix given its Cholesky upper Triangular decomposition of matrix
        res = matrix([[]])
        res.zero(self.dimx, self.dimy)
        # backward step for inverse
        for j in reversed(range(self.dimx)):
            tjj = self.value[j][j]
            temp = [self.value[j][k] * res.value[j][k] for k in range(j+1, self.dimx)]
            s = sum(temp)
            res.value[j][j] = 1./tjj**2 - s/tjj
        for i in reversed(range(j)):
            res.value[j][i] = res.value[i][j] = -sum([self.value[i][k]*res.value[k][j] for k in range(i+1,self.dimx)])/self.value[i][i]
        return res
    
    def inverse(self):
        aux = self.Cholesky()
        res = aux.CholeskyInverse()
        return res
    
    def __repr__(self):
        return repr(self.value)