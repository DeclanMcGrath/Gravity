import math
from pointMass import PointMass
from vector import Vector
from render3d import canvas

def main():
    vec = Vector(1,2,3)
    print(vec.getMass())
    canvas(600, 480, 10)
