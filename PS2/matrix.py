'''
Created on May 23, 2017

@author: Xing Wang
'''
import math

class matrix(object):
    '''
    implements basic operations of a matrix class
    '''
    DIAG_CLASS = "matrix."

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
        # Check if dimensions are Valid
        if dimx < 1 or dimy < 1:
            raise ValueError, "Invalid size of matrix"
        else:
            self.dimx = dimx
            self.dimy = dimy
            self.value = [[0 for row in range(dimy)] for col in range(dimx)]
            
    def identify(self, dim):
        # Check if dimensions are Valid
        if dim < 1:
            raise ValueError, "Invalid size of matrix"
        else:
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
        # Check if dimensions are Valid
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError, "Matrices must be of equal dimensions to add"
        else:
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] + other.value[i][j]
            return res
        
    def __sub__(self, other):
        # Check if dimensions are Valid
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError, "Matrices must be of equal dimensions to subtract" 
        else:
            res = matrix([[]])
            res.zero(self.dimx, self.dimy) 
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] - other.value[i][j]
            return res
        
    def __mul__(self, other):
        # Check if dimensions are Valid
        if self.dimy != other.dimx:
            raise ValueError, "Matrices must be mxn and nxp to multiply"
        else:
            res = matrix([[]])
            res.zero(self.dimx, other.dimy)
            for i in range(self.dimx):
                for j in range(other.dimy):
                    pass
            return res
        
    def transpose(self):
        res = matrix([[]])
        res.zero(self.dimy, self.dimx)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res.value[i][j] = self.value[j][i]
        return res
    
    def Cholesky(self, ztol = 1e-5):
        # Computes the upper triangular Cholesky factorization of a positive definite matrix
        res = matrix([[]])
        res.zero(self.dimx, self.dimy)
        for i in range(self.dimx):
            S = sum([(res.value[k][i])**2 for k in range(i)])
            d = self.value[i][i] - S 
            if abs(d) < ztol:
                res.value[i][i] = 0.
            else:
                if d < 0.:
                    raise ValueError, "Matrix is not positive definite"
                res.value[i][i] = math.sqrt(d)
            for j in range(i+1, self.dimx):
                S = sum([res.value[k][i] * res.value[k][j] for k in range(self.dimx)])
                if abs(S) < ztol:
                    S = 0. 
                res.value[i][j] = (self.value[i][j] - S) / res.value[i][i]
        return res
    
    def CholeskyInverse(self):
        # Computes inverse of a matrix given its Cholesky upper triangular decomposition of matrix
        res = matrix([[]])
        res.zero(self.dimx, self.dimy)
        # Backward step for inverse.
        for j in reversed(range(self.dimx)):
            tjj = self.value[j][j]
            S = sum([self.value[j][k]*res.value[j][k] for k in range(j+1, self.dimx)])
            res.value[j][j] = 1. / tjj**2 - S/tjj
            for i in reversed(range(j)):
                res.value[j][i] = res.value[i][j] = -sum([self.value[i][k]*res.value[k][j] for k in range(i+1, self.dimx)])/self.value[i][i]
        return res
    
    def inverse(self):
        aux = self.Cholesky()
        res = aux.CholeskyInverse()
        return res
    
    def __repr__(self):
        return repr(self.value)