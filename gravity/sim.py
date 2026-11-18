import math
from pointMass import PointMass
from vector import Vector

class Sim:
    G = 6.6743 * pow(10, -11) # get scipy and put in the actual G number
    
    def __init__(self, points):
        self.points = points

    def calcGravAccel(pm1, pm2): # F_g = G * m1 * m2 / r^2  ∴  a = G * m1 / r^2
        gravAccel = []
        for i in range(0,3):
            if(pm1.getPosVec().getCartesian()[0] - pm2.getPosVec().getCartesian()[0] != 0): # checks to make sure the coord dif isn't 0. Avoids / by 0 error
                gravAccel.append(Sim.G * pm2.getMass() / pow(pm1.getPosVec().getCartesian()[0] - pm2.getPosVec().getCartesian()[0], 2))
            else:
                gravAccel.append(0) # if the coord dif IS 0, it appends 0 bc there will be no attraction in that direction
        return gravAccel
    
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
    
    def stopSim(self): # you should kill yourself NOW!!
        del self

"""            
pt1 = PointMass(Vector([1,2,3]),Vector([1,2,3]),1000000000000000,1)
pt2 = PointMass(Vector([3,4,5]),Vector([6,4,2]),2000000000000000,1)
pt3 = PointMass(Vector([6,7,8]),Vector([9,9,9]),3000000000000000,1)
pt4 = PointMass(Vector([9,10,11]),Vector([1,0,1]),4000000000000000,1)

sim = Sim([pt1, pt2, pt3, pt4])

sim.update()
"""