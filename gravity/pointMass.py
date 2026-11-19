import math
from vector import Vector

class PointMass:
    def __init__(self, posVec, velVec, mass, radius, surfaceTemp):
        self.posVec = posVec 
        self.velVec = velVec 
        self.mass = mass 
        self.radius = radius 
        self.surfaceTemp = surfaceTemp
    
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
    def getDensity(self): # kg/m^3
        return self.mass / (4 / 3 * math.pi * pow(self.radius, 2))
    def getSurfaceTemp(self):
        return self.surfaceTemp

