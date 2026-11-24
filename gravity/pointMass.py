import math
from vector import Vector

class PointMass:
    def __init__(self, posVec, velVec, mass, radius, surfaceTemp):
        self.posVec = posVec 
        self.velVec = velVec 
        self.mass = mass 
        self.radius = radius 
        self.surfaceTemp = surfaceTemp
    
    def nextFrame(self, accVec, dt=0.05):
        self.velVec.changeXYZ(accVec.scaled(dt))
        self.posVec.changeXYZ(self.velVec.scaled(dt))

    def getPosVec(self):
        return self.posVec
    def getVelVec(self):
        return self.velVec 
    def getMass(self):
        return self.mass 
    def getRadius(self):
        return self.radius
    def getDensity(self): # kg/m^3
        return self.mass / (4 / 3 * math.pi * pow(self.radius, 3))
    def getSurfaceTemp(self):
        return self.surfaceTemp
    def __str__(self):
        return f"{self.posVec},{self.velVec},{self.mass},{self.radius},{self.surfaceTemp}"

