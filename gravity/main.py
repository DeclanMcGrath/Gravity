from pointMass import PointMass
from vector import Vector
from render3d import Canvas
from sim import Sim


def main():
    sun = PointMass(Vector([0,0,0]), Vector([0, -0.216, -0.049]), 10**12, 1, -1)


    pt1 = PointMass(Vector([6,0,0]),  Vector([0, 3.34, 0.00]),  10000000000, 1, -1)
    pt2 = PointMass(Vector([9,0,0]),  Vector([0, 2.56, 0.93]),  20000000000, 1, -1)
    pt3 = PointMass(Vector([12,0,0]), Vector([0, 2.22, -0.81]), 30000000000, 1, -1)
    pt4 = PointMass(Vector([15,0,0]), Vector([0, 1.62, 1.36]),  40000000000, 1, -1)

    sim = Sim([sun, pt1, pt2, pt3, pt4])

    canvas = Canvas(720, 600, 16, sim)

    canvas.run()

if __name__ == "__main__":
    main()
