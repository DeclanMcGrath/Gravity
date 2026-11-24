import math
from pointMass import PointMass
from vector import Vector

class Sim:
    G = 6.6743 * pow(10, -11) # get scipy and put in the actual G number
    
    def __init__(self, points):
        self.points = points

    @staticmethod
    def calcGravAccel(pm1, pm2): # F_g = G * m1 * m2 / r^2  ∴  a = G * m1 / r^2
        p1 = pm1.getPosVec().getCartesian()
        p2 = pm2.getPosVec().getCartesian()
        diff = [p2[i] - p1[i] for i in range(3)]
        r = math.sqrt(sum(d * d for d in diff) + 0.25)   # +0.25 softner for close encounters between bodies
        return [Sim.G * pm2.getMass() * d / r ** 3 for d in diff]
    
    @staticmethod
    def calcCenterMass(points):
        toReturn = []
        for i in range(0,3):
            centerMass = 0
            totalMass = 0
            for point in points:
                centerMass += point.getMass() * point.getPosVec().getCartesian()[i]
                totalMass += point.getMass()
            toReturn.append(centerMass / totalMass)
        return toReturn
    
    def update(self):
        pointUpdated = []
        for point in self.points: # fills pointUpdated with new points that are the updated versions of the points in self.points
            accel = Vector([0,0,0])
            for mPoint in self.points:
                acc = Vector(Sim.calcGravAccel(point, mPoint))
                accel.changeXYZ(acc)
                del acc
            mPoint = point
            mPoint.nextFrame(accel)
            del accel
            pointUpdated.append(mPoint)
        for i in range(0, len(self.points)): # fills self.points with the points from pointUpdated
            self.points[i] = pointUpdated[i]
        del pointUpdated
    
    def getPoints(self):
        return self.points

    def stopSim(self): # you should kill yourself NOW!!
        del self

"""
pt1 = PointMass(Vector([1,2,3]),Vector([1,2,3]),10000000000,1, -1)
pt2 = PointMass(Vector([3,4,5]),Vector([6,4,2]),20000000000,1, -1)
pt3 = PointMass(Vector([6,7,8]),Vector([9,9,9]),30000000000,1, -1)
pt4 = PointMass(Vector([9,10,11]),Vector([1,0,1]),40000000000,1, -1)

sim = Sim([pt1, pt2, pt3, pt4])

print(Sim.calcCenterMass(sim.points))
"""