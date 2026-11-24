from sdl3 import *
from ctypes import byref
from collections import deque
import math

##------file imports------##
from sim import Sim
from camera3d import Camera

class Canvas:
    def __init__(self, x, y, tickSpeed, sim):

        ##--- intialize values ---##
        self.sizeX = x 
        self.sizeY = y 
        self.sim = sim
        self.tickSpeed = tickSpeed
        self.offsets = []
        self.sunRadius = 40
        self.trailLength = 150      # number of past positions kept per planet
        self.trails = {}            # body index -> deque of (x, y, z) offsets

        ## setup camera
        self.camera = Camera(0, 0, -30, 0.0, 0.3)
        self.camera.setScreen(x, y, focal=600)
        self.camera.orbit(0, 0, 0) ##place camera around center of mass


        ##error handler
        if not SDL_Init(SDL_INIT_VIDEO):
            raise RuntimeError(f"SDL_Init Error: {self._err()}")
        
        ##create a new window
        self.window = SDL_CreateWindow(b"Gravity Sim", self.sizeX, self.sizeY, 0)

        ## error handler
        if not self.window:
            SDL_DestroyWindow(self.window)
            SDL_Quit()
            raise RuntimeError(f"SDL_CreateWindow Error: {self._err()}")

        ##create the rendering tool
        self.renderer = SDL_CreateRenderer(self.window, None)
        if not self.renderer:
            SDL_DestroyWindow(self.window)
            SDL_Quit()
            raise RuntimeError(f"SDL_CreateRenderer Error: {self._err()}")

    def _err(self):
        e = SDL_GetError()
        return e.decode("utf-8") if isinstance(e, bytes) else e
    
    ##------ main loop ------##
    def run(self):
        self.running = True
        self.event = SDL_Event()
        
        while self.running:
            while SDL_PollEvent(byref(self.event)):
                if self.event.type == SDL_EVENT_QUIT:
                    self.running = False

            self.handleInput()
            self.sim.update()
            self.createOffsets()
                    
            SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
            SDL_RenderClear(self.renderer)
            self.drawTrails()
            self.drawBodies()
            # Present the drawn frame to the screen
            SDL_RenderPresent(self.renderer)
            SDL_Delay(self.tickSpeed)
        self.close()


    def close(self):
        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)
        SDL_Quit()


    ##------ camera ------##
    def handleInput(self):
        keys = SDL_GetKeyboardState(None)
        dRot = dPitch = dDist = 0.0
        if keys[SDL_SCANCODE_LEFT]:
            dRot -= 0.03
        if keys[SDL_SCANCODE_RIGHT]:
            dRot += 0.03
        if keys[SDL_SCANCODE_UP]:
            dPitch -= 0.03
        if keys[SDL_SCANCODE_DOWN]:
            dPitch += 0.03
        if keys[SDL_SCANCODE_W]:
            dDist -= 0.5
        if keys[SDL_SCANCODE_S]:
            dDist += 0.5
        if dRot or dPitch or dDist:
            # offsets are relative to the center of mass, which sits at (0, 0, 0)
            self.camera.orbit(0, 0, 0, dRot, dPitch, dDist)

    ##------ draw bodies ------##
    def createOffsets(self):
        ##each body's position relative to the sun (body 0)
        points = self.sim.getPoints()
        sun = points[0].getPosVec().getCartesian()
        self.offsets = []
        for pm in points:
            x, y, z = pm.getPosVec().getCartesian()
            self.offsets.append((x - sun[0], y - sun[1], z - sun[2], pm.getMass()))

        for i, (ox, oy, oz, mass) in enumerate(self.offsets):
            if i == 0:              # skip the sun
                continue
            trail = self.trails.setdefault(i, deque(maxlen=self.trailLength))
            trail.append((ox, oy, oz))

    PLANET_COLORS = [(90, 160, 255), (120, 220, 130), (240, 120, 120), (200, 160, 255)]

    def drawBodies(self):
        drawList = []

        for i, (ox, oy, oz, mass) in enumerate(self.offsets):
            p = self.camera.project(ox, oy, oz)
            if not p:
                continue
            if i == 0:                                   # body 0 is the sun
                drawList.append(("sun", p, self.sunRadius, None))
            else:
                color = self.PLANET_COLORS[(i - 1) % len(self.PLANET_COLORS)]
                radius = max(2, (mass ** (1 / 3) / 400) * p[2] / 20)
                drawList.append(("planet", p, radius, color))

        drawList.sort(key=lambda item: -item[1][3])      # farthest first

        for kind, (sx, sy, scale, depth), radius, color in drawList:
            if kind == "sun":
                self.renderStep(self.renderer, sx, sy, radius * scale / 20)
            else:
                self.drawPlanet(sx, sy, radius, color)

    def drawPlanet(self, sx, sy, radius, color):
        r, g, b = color
        SDL_SetRenderDrawColor(self.renderer, r, g, b, 255)
        self.fillCircle(self.renderer, sx, sy, radius)
        # small highlight so it reads as a sphere
        SDL_SetRenderDrawColor(self.renderer, min(255, r + 80), min(255, g + 80), min(255, b + 80), 255)
        self.fillCircle(self.renderer, sx - radius * 0.3, sy - radius * 0.3, max(1, radius * 0.35))

    ##------ drawing ------##
    def fillCircle(self, renderer, pointMassX, pointMassY, pointMassRadius):
        pointMassX, pointMassY, pointMassRadius = int(pointMassX), int(pointMassY), int(pointMassRadius)
        for dy in range (-pointMassRadius, pointMassRadius +1):
            dx = int(math.sqrt(pointMassRadius * pointMassRadius - dy * dy))
            SDL_RenderLine(renderer, pointMassX - dx, pointMassY + dy, pointMassX + dx, pointMassY + dy)

    def glowCircle(self, renderer, pointMassX, pointMassY, pointMassRadius, color=(255, 200, 50), strength=0.8, step=2):
        pointMassRadius = int(pointMassRadius)
        if pointMassRadius < 1:
            return
        SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_ADD)

        r, g, b = color
        ##slice up each ring and change the color
        for i in range(pointMassRadius, 0, -step):      # step=2 skips rings for speed
            t = 1 - i / pointMassRadius
            a = min(255, int(255 * t ** 2 * strength * step))
            SDL_SetRenderDrawColor(renderer, r, g, b, a)
            self.fillCircle(renderer, pointMassX, pointMassY, i)

        SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_NONE)

    def renderStep(self, renderer, pointMassX, pointMassY, pointMassRadius):
        ##render the sun at the center of mass
        self.glowCircle(renderer, pointMassX, pointMassY, pointMassRadius * 3, color=(255, 90, 20), strength=0.5)
        self.glowCircle(renderer, pointMassX, pointMassY, pointMassRadius * 2, color=(255, 160, 40), strength=0.6)
        self.glowCircle(renderer, pointMassX, pointMassY, pointMassRadius * 0.75, color=(255, 230, 150), strength=0.8)
        SDL_SetRenderDrawColor(renderer, 255, 255, 220, 255)
        self.fillCircle(renderer, pointMassX, pointMassY, pointMassRadius // 3)

    def drawTrails(self):
        SDL_SetRenderDrawBlendMode(self.renderer, SDL_BLENDMODE_BLEND)
        for i, trail in self.trails.items():
            r, g, b = self.PLANET_COLORS[(i - 1) % len(self.PLANET_COLORS)]
            n = len(trail)
            prev = None
            for k, (ox, oy, oz) in enumerate(trail):
                p = self.camera.project(ox, oy, oz)
                if p and prev:
                    alpha = int(200 * k / n)            # oldest = transparent, newest = brighter
                    SDL_SetRenderDrawColor(self.renderer, r, g, b, alpha)
                    SDL_RenderLine(self.renderer, prev[0], prev[1], p[0], p[1])
                prev = p
        SDL_SetRenderDrawBlendMode(self.renderer, SDL_BLENDMODE_NONE)

