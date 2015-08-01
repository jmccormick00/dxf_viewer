# -*- coding: utf-8 *-*

import math


class vector3D:
    '''A class for representing a 3D vector'''

    zero_tolerance = 0.0001

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x, self.y, self.z = x, y, z

    def copy(self):
        return vector3D(self.x, self.y, self.z)

    def length(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y) +
                        (self.z * self.z))

    def lengthSquared(self):
        return (self.x * self.x) + (self.y * self.y) + (self.z * self.z)

    def reverse(self):
        self.x = -self.x
        self.y = -self.y
        self.z = -self.z

    def normalize(self):
        c = self.length()
        if(c <= self.zero_tolerance):
            c = 1.0
        self.x /= c
        self.y /= c
        self.z /= c

        if(math.fabs(self.x) < self.zero_tolerance):
            self.x = 0.0
        if(math.fabs(self.y) < self.zero_tolerance):
            self.y = 0.0
        if(math.fabs(self.z) < self.zero_tolerance):
            self.z = 0.0

    def normalizeVector(self):
        a = self.x
        b = self.y
        c = self.z
        d = self.length()
        if(d <= self.zero_tolerance):
            d = 1.0
        a /= d
        b /= d
        c /= d
        if(math.fabs(a) < self.zero_tolerance):
            a = 0.0
        if(math.fabs(b) < self.zero_tolerance):
            b = 0.0
        if(math.fabs(c) < self.zero_tolerance):
            c = 0.0
        return vector3D(a, b, c)

    def crossProduct(self, v):
        return vector3D((self.y * v.z - self.z * v.y),
            (-self.x * v.z + self.z * v.x), (self.x * v.y - self.y * v.x))

    def dotProduct(self, v):
        return (self.x * v.x) + (self.y * v.y) + (self.z * v.z)

    def __add__(self, v):
        '''Add two vectors together v1 + v2'''
        return vector3D(self.x + v.x, self.y + v.y, self.z + v.z)

    def __sub__(self, v):
        '''subtract v from current v1 - v2'''
        return vector3D(self.x - v.x, self.y - v.y, self.z - v.z)

    def __div__(self, d):
        '''divide a vector by a scalar and return a new vector'''
        return vector3D(self.x / float(d), self.y / float(d), self.z / float(d))

    def __eq__(self, v):
        '''v1 == v2'''
        if(self.x != v.x):
            return False
        if(self.y != v.y):
            return False
        if(self.z != v.z):
            return False
        return True

    def __ne__(self, v):
        '''v1 != v2'''
        if(self.x != v.x):
            return True
        if(self.y != v.y):
            return True
        if(self.z != v.z):
            return True
        return False

    def __mul__(self, f):
        '''multiply the current vector by a factor'''
        return vector3D(self.x * f, self.y * f, self.z * f)

    def __iadd__(self, v):
        '''adds v to the current vector and returns self (self += v)'''
        self.x += v.x
        self.y += v.y
        self.z += v.z
        return self

    def __isub__(self, v):
        '''subtracts v from current and returns self (self -= v)'''
        self.x -= v.x
        self.y -= v.y
        self.z -= v.z
        return self

    def __imul__(self, f):
        '''multiply the current vector by a factor (self *= f)'''
        self.x *= f
        self.y *= f
        self.z *= f
        return self

    def __idiv__(self, f):
        '''multiply the current vector by a factor (self *= f)'''
        self.x /= float(f)
        self.y /= float(f)
        self.z /= float(f)
        return self

    def __neg__(self):
        '''Negate the current vector'''
        return vector3D(-self.x, -self.y, -self.z)

    def __repr__(self):
        return "Vec3D(%f, %f, %f)" % (self.x, self.y, self.z)
