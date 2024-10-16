import pygame
from Scripts.animation import Animation
import time
class Player:

    def __init__(self, screen:pygame.display, pos_X:int, pos_Y:int, gravity:float, speed:int, controls:str, spriteDir:str, clock:pygame.time.Clock, fps:int):
        self.x = pos_X
        self.y = pos_Y
        
        self.g = gravity
        self.speed = speed

        self.controls = controls
        
        self.spriteDir = spriteDir

        self.screen = screen

        self.clock = clock

        self.fps = fps

        self.idle = Animation(self.screen, self.spriteDir+"\\"+r"\idle", self.x, self.y, 0.05, self.clock, self.fps, (100, 100), True, "idle")
        self.running = Animation(self.screen, self.spriteDir+"\\"+r"running", self.x, self.y, 0.025, self.clock, self.fps, (100, 100), True, "running")
        self.rolling = Animation(self.screen, self.spriteDir+"\\"+r"rolling", self.x, self.y, 0.025, self.clock, self.fps, (100, 100), False)
        self.hit= Animation(self.screen, self.spriteDir+"\\"+r"hit", self.x, self.y, 0.025, self.clock, self.fps, (100, 100), False)
        self.death = Animation(self.screen, self.spriteDir+"\\"+r"death", self.x, self.y, 0.025, self.clock, self.fps, (100, 100), False)
        self.currentAnimation:Animation = self.idle

        self.animations = [self.idle, self.running, self.rolling, self.hit, self.death]

        self.vY = 0

    def chooseAnimation(self, animation):
        # if animation == self.currentAnimation or (self.currentAnimation == "hit" and self.currentAnimation.finished == False):
        #     pass
        
        self.currentAnimation = animation
            
    def lookLeft(self):
        for elt in self.animations:
            elt.lookdir = -1

    def lookRight(self):
        for elt in self.animations:
            elt.lookdir = 1

    def update(self, deltaTime):
        self.addGravity(deltaTime)

    

    def addGravity(self, deltaTime):
        self.vY += self.g * deltaTime
        self.y += self.vY
        
    def Playidle(self):
        for elt in self.animations:
            elt.active = False
        self.idle.active = True
    
    def notIdle(self):
        for elt in self.animations:
            elt.active = True
        self.idle.active = False

    def idleAnimation(self):
        self.currentAnimation.animate()

        for elt in self.animations:
            elt.x = self.x
            elt.y = self.y

        self.currentAnimation.x = self.x
        self.currentAnimation.y = self.y


    def keys(self, deltaTime):
        # self.addGravity(deltaTime)

        pressed_keys = pygame.key.get_pressed()
        keysToReturn = {}



        if pressed_keys[int(self.controls["left"])]:
            keysToReturn["left"] = True
        else:
            keysToReturn["left"] = False

        if pressed_keys[int(self.controls["right"])]:
            keysToReturn["right"] = True
        else:
            keysToReturn["right"] = False
        
        if pressed_keys[int(self.controls["up"])]:
            keysToReturn["up"] = True
        else:
            keysToReturn["up"] = False

        if pressed_keys[int(self.controls["down"])]:
            keysToReturn["down"] = True
        else:
            keysToReturn["down"] = False

        if pressed_keys[int(self.controls["jump"])]:
            keysToReturn["jump"] = True
        else:
            keysToReturn["jump"] = False

        if pressed_keys[int(self.controls["exit"])]:
            keysToReturn["exit"] = True
        else:
            keysToReturn["exit"] = False

        return keysToReturn

