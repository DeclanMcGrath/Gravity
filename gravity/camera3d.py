import math

class Camera:
    
    def __init__(self, posX, posY, posZ, rotAngle, pitchAngle):
        self.x = posX
        self.y = posY
        self.z = posZ
        self.rot = rotAngle
        self.pitch = pitchAngle
        self.dist = 30.0
        self.focal = 600.0
        self.screenW = 800
        self.screenH = 600

    def setScreen(self, width, height, focal=None):
        self.screenW = width
        self.screenH = height

        if focal is not None:
            self.focal = focal

    def moveCam(self, newX, newY, newZ):
        self.x = newX
        self.y = newY
        self.z = newZ

    def pointTowards(self, pX, pY, pZ):
        dx = pX = self.x
        dy = pY - self.y
        dz = pZ - self.z

        self.rot = math.atan2(dx, dz)
        self.pitch = math.atan2(dy, math.hypot(dx, dz))

    def forward(self):
        cp = math.cos(self.pitch)
        return (math.sin(self.rot) * cp, math.sin(self.pitch), math.cos(self.rot) * cp)
    
    def orbit(self, tx, ty, tz, dRot = 0.0, dPitch = 0.0, dDist = 0.0):
        ##Rotate/zoom around a target point and keep looking at it.
        self.rot += dRot
        self.pitch = max(-1.5, min(1.5, self.pitch + dPitch))
        self.dist = max(2.0, self.dist + dDist)
        fx, fy, fz = self.forward()
        self.x = tx - fx * self.dist
        self.y = ty - fy * self.dist
        self.z = tz - fz * self.dist

    def worldToCamera(self, wx, wy, wz):
        dx, dy, dz = wx-self.x, wy-self.y, wz - self.z

        #calc yaw
        cr, sr = math.cos(self.rot), math.sin(self.rot)
        x1 = dx * cr - dz * sr
        z1 = dx * sr + dz * cr

        #calc pitch
        cp, sp = math.cos(self.pitch), math.sin(self.pitch)
        y2 = dy * cp - z1 * sp
        z2 = dy * sp + z1 * cp
        return x1, y2, z2

    def project(self, wx, wy, wz):
        ##returns screenX, screenY, scale depth or None if behind the camera
        x, y, depth = self.worldToCamera(wx, wy, wz)
        if depth < 0.1:
            return None
        scale = self.focal/depth
        return self.screenW / 2 + x * scale, self.screenH / 2 + y * scale, scale, depth
    
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getZ(self):
        return self.z
    