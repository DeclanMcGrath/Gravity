import math
from vector import Vector

class Camera:
    
    def __init__(self, posX, posY, poZ, rotAngle, pitchAngle):
        self.x = posX
        self.y = posY
        self.z = poZ
        self.rot = rotAngle
        self.pitch = pitchAngle

    def moveCam(self, newX, newY, newZ):
        self.x = newX
        self.y = newY
        self.z = newZ

    def pointTowards(self, pX, pY, pZ):
        distanceX = pX = self.x
        distanceY = pY - self.y
        distanceZ = pZ - self.z

        self.rot = math.sin(distanceX/distanceY)
        self.pitch = math.sin(distanceZ/distanceY)

    
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getZ(self):
        return self.z
    