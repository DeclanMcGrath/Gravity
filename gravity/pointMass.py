import math
from vector import Vector

class PointMass:
    def __init__(self, posVec, velVec, mass, radius):
        self.posVec = posVec 
        self.velVec = velVec 
        self.mass = mass 
        self.radius = radius 
    
    def nextFrame(self, accVec):
        self.velVec.changeXYZ(accVec)
        self.posVec.changeXYZ(self.velVec)

    def getPosVec(self):
        return self.posVec
    def getVelVec(self):
        return self.velVec 
    def getMass(self):
        return self.mass 
    def getRadius(self):
        return self.radius
