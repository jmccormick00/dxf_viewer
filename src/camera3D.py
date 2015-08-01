# -*- coding: utf-8 *-*

import math
from OpenGL.GLU import *
#from vector3D import vector3D


class camera3D:
    '''
    Defines a camera that has the ability to move around in a 3D environment
    The camera is not free roaming.  It is fixed to look at a target.
    Gives the user the ability to pan, orbit, and zoom in relation to a target
    '''

    def __init__(self, pos, target, camUp, sceneUp):
        self.pos = pos
        self.target = target
        self.camUp = camUp
        self.sceneUp = sceneUp

        self.sceneUp.normalize()
        self.camUp.normalize()

        # Calculate the side vector
        look = self.target - self.pos
        self.sideVector = look.crossProduct(self.camUp)
        self.sideVector.normalize()

    def updateCamera(self):
        gluLookAt(self.pos.x, self.pos.y, self.pos.z,
                self.target.x, self.target.y, self.target.z,
                self.camUp.x, self.camUp.y, self.camUp.z)

    def panHorizontal(self, x):
        self.pos += (self.sideVector * x)
        self.target += (self.sideVector * x)

    def panVertical(self, y):
        self.pos += (self.camUp * y)
        self.target += (self.camUp * y)

    def zoomCamera(self, amt):
        look = self.target - self.pos
        length = look.length()
        look.normalize()

        temp = look * amt
        len2 = temp.length()

        if(amt > 0.0):
            if((length - len2) > 1.0):
                self.pos += temp
        else:
            self.pos += temp

    def orbitX(self, amt):
        look = self.target - self.pos
        r = look.length()
        w = r - (r * math.cos(amt))
        h = r * math.sin(amt)

        look.normalize()
        self.pos += ((look * w) + (self.sideVector * h))

        # update the side vector
        look = self.target - self.pos
        self.sideVector = look.crossProduct(self.camUp)
        self.sideVector.normalize()

    def orbitY(self, amt):
        look = self.target - self.pos
        r = look.length()
        w = r - (r * math.cos(amt))
        h = r * math.sin(amt)

        look.normalize()
        self.pos += ((look * w) + (self.camUp * h))

        # update the up vector
        look = self.target - self.pos
        self.camUp = self.sideVector.crossProduct(look)
        self.camUp.normalize()
