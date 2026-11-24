import math

class Vector:
    def __init__(self, args):
        self.x = args[0]
        self.y = args[1]
        self.z = args[2]
    
    def getSpherical(self):
        mRho = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))
        if mRho == 0:
            return [0, 0, 0]
        mPhi = math.acos(self.z / mRho)
        mTheta = math.atan2(self.y, self.x)
        return [mRho, mTheta, mPhi]
    
    def getCartesian(self):
        return [self.x, self.y, self.z]

    def setXYZ(self, val):
        self.x, self.y, self.z = val.getCartesian()

    def changeXYZ(self, val):
        self.x += val.getCartesian()[0]
        self.y += val.getCartesian()[1]
        self.z += val.getCartesian()[2]
    
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
    
    def subtract(self, other):
        return Vector([self.x - other.x, self.y - other.y, self.z - other.z])

    def scaled(self, k):
        return Vector([self.x * k, self.y * k, self.z * k])
