import math

class Camera:
    
    def __init__(self, posX, posY, posZ, rotAngle, pitchAngle, screenW, screenH):
        self.x = posX
        self.y = posY
        self.z = posZ
        self.rot = rotAngle
        self.pitch = pitchAngle
        self.dist = 30.0
        self.focal = 600.0
        self.screenW = screenW
        self.screenH = screenH

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
    