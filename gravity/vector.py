import math
from typing import overload

class Vector:
    def __init__(self, args):
        self.x = args[0]
        self.y = args[1]
        self.z = args[2]
    
    def getSpherical(self):
        mRho = math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))
        mPhi = math.acos(self.z / mRho)
        mTheta = math.acos(self.x / (mRho * math.sin(mPhi)))
        return [mRho, mTheta, mPhi]
    
    def getCartesian(self):
        return [self.x, self.y, self.z]

    def setXYZ(self, val):
        self.x = val.getCartesian()[0]
        self.y = val.getCartesian()[1]
        self.z = val.getCartesian()[2]

    def changeXYZ(self, val):
        self.x += val.getCartesian()[0]
        self.y += val.getCartesian()[1]
        self.z += val.getCartesian()[2]
