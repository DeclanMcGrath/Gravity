import sys
from sdl2 import *
from ctypes import byref
import math
from pointMass import PointMass
from vector import Vector

class canvas:
    def __init__(self, X, Y, tickSpeed):
        self.sizeX = X
        self.sizeY = Y
        ##intialize the library
        if SDL_Init(SDL_INIT_VIDEO) !=0:
            print(f"SDL_Init Error: {SDL_GetError().decode('utf-8')}")
            return
        
        ##create a new window
        self.window = SDL_CreateWindow(
            b"Gravity Sim",
            SDL_WINDOWPOS_CENTERED,
            SDL_WINDOWPOS_CENTERED,
            self.sizeX, self.sizeY,
            SDL_WINDOW_SHOWN
        )

        ## if the window failes to be created
        if not self.window:
            print(f"SDL_CreateWindow Error: {SDL_GetError().decode('utf-8')}")
            SDL_DestroyWindow(self.window)
            SDL_Quit()
            return

        ##create the rendering tool
        self.renderer = SDL_CreateRenderer(self.window, -1, SDL_RENDERER_ACCELERATED)
        if not self.renderer:
            print(f"SDL_CreateRenderer Error: {SDL_GetError().decode('utf-8')}")
            SDL_DestroyWindow(self.window)
            SDL_Quit()
            return

        
    def run(self):
        self.running = True
        self.event = SDL_Event()
        
        while self.running:
            while SDL_PollEvent(byref(self.event)) != 0:
                if self.event.type == SDL_QUIT:
                    self.running = False
                    
            SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
            SDL_RenderClear(self.renderer)

            SDL_SetRenderDrawColor(self.renderer, 255, 200, 50, 255)
            self.renderStep(self.renderer, 400, 300, 50)
            
            # Present the drawn frame to the screen
            SDL_RenderPresent(self.renderer)
            SDL_Delay(16)
        self.close()


    def close(self):
        SDL_DestroyRenderer(self.renderer)
        SDL_DestroyWindow(self.window)
        SDL_Quit()

    def fillCircle(self, renderer, pointMassX, pointMassY, pointMassRadius):
        pointMassX, pointMassY, pointMassRadius = int(pointMassX), int(pointMassY), int(pointMassRadius)
        for dy in range (-pointMassRadius, pointMassRadius +1):
            dx = int(math.sqrt(pointMassRadius * pointMassRadius - dy * dy))
            SDL_RenderDrawLine(renderer, pointMassX - dx, pointMassY + dy, pointMassX + dx, pointMassY + dy)

    def glowCircle(self, renderer, pointMassX, pointMassY, pointMassRadius, color=(255, 200, 50)):
        SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_ADD)

        r, g, b = color
        ##slice up each ring and change the color
        for i in range(int(pointMassRadius), 0, -1):
            t = 1 - i / pointMassRadius
            a = int(255 * t ** 2 * 0.8) 
            SDL_SetRenderDrawColor(renderer, r, g, b, a)

            self.fillCircle(renderer, pointMassX, pointMassY, i)

    def renderStep(self, renderer, pointMassX, pointMassY, pointMassRadius):
        self.glowCircle(renderer, pointMassX, pointMassY, pointMassRadius * 3, color=(255, 120, 30))   # wide, dim outer halo
        self.glowCircle(renderer, pointMassX, pointMassY, pointMassRadius * 1.5, color=(255, 200, 50))   # mid glow
        self.glowCircle(renderer, pointMassX, pointMassY, pointMassRadius * 0.75, color=(255, 255, 200))
        SDL_SetRenderDrawColor(self.renderer, 255, 255, 220, 255)
        self.fillCircle(renderer, pointMassX, pointMassY, pointMassRadius // 2)

if __name__ == "__main__":
    canvas(800, 600, 10).run()
