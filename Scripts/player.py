import pygame
from Scripts.animation import Animation
import time
class Player:

    def __init__(self, screen:pygame.display, tilesize:int, pos_X:int, pos_Y:int, gravity:float, speed:int, jumpforce:float, controls:str, spriteDir:str, clock:pygame.time.Clock, fps:int):
        self.x:int = pos_X
        self.y:int = pos_Y
        
        self.jumpForce:float = jumpforce

        self.tilesize:int = tilesize

        self.g:float = gravity
        self.speed:int = speed

        self.controls:str = controls
        
        self.spriteDir:str = spriteDir

        self.screen:pygame.Surface = screen

        self.clock:pygame.time.Clock = clock

        self.fps:int = fps

        self.beatLevel:bool = False

        self.grounded:bool = False

        self.idle:Animation = Animation(self.screen, self.spriteDir+"\\"+r"\idle", self.x, self.y, 0.15, self.clock, self.fps, (100, 100), True, "idle", 25, 75)
        self.running:Animation = Animation(self.screen, self.spriteDir+"\\"+r"running", self.x, self.y, 0.05, self.clock, self.fps, (100, 100), True, "running", 25, 75)
        self.rolling:Animation = Animation(self.screen, self.spriteDir+"\\"+r"rolling", self.x, self.y, 0.025, self.clock, self.fps, (100, 100), False, 25, 75)
        self.hit:Animation = Animation(self.screen, self.spriteDir+"\\"+r"hit", self.x, self.y, 0.025, self.clock, self.fps, (100, 100), False, 25, 75)
        self.death:Animation = Animation(self.screen, self.spriteDir+"\\"+r"death", self.x, self.y, 0.025, self.clock, self.fps, (100, 100), False, 25, 75)
        self.falling:Animation = Animation(self.screen, self.spriteDir+"\\"+r"falling", self.x, self.y, 0.0175, self.clock, self.fps, (100, 100), False, "falling", 25, 75)
        self.currentAnimation:Animation = self.idle

        self.animations:list[Animation] = [self.idle, self.running, self.rolling, self.hit, self.death, self.falling]

        self.vY:float = 0

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

    
    def doCollisions(self, collisions):
        thing_to_test = pygame.Rect(self.x+11, self.y+10, 27, 55).collidelistall(collisions)
        if thing_to_test != []:
            return (True, thing_to_test)
        return (False, 0)
    
    def update(self, deltaTime, collisions):
        if self.doCollisions(collisions)[0] == False:
            self.addGravity(deltaTime)
            self.grounded = False
            col = self.doCollisions(collisions)
            if col[0] and self.vY >= 0:
                self.y = collisions[col[1][0]].y - 60
                self.vY = 0
                self.grounded = True
            if col[0] and self.vY < 0:
                self.vY = 20
                self.addGravity(deltaTime) 
    
    def jump(self, deltaTime):
        self.vY -= self.g * deltaTime * self.jumpForce
        self.addGravity(deltaTime)

    def addGravity(self, deltaTime):
        self.vY += self.g * deltaTime * 2.5
        if(self.vY > -4):
            self.vY += self.g * deltaTime * 8
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

        self.currentAnimation.x = self.x
        self.currentAnimation.y = self.y


    def keys(self):
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

        if pressed_keys[int(self.controls["switch"])]:
            keysToReturn["switch"] = True
        else:
            keysToReturn["switch"] = False

        if pressed_keys[int(self.controls["copy"])]:
            keysToReturn["copy"] = True
        else:
            keysToReturn["copy"] = False
        
        if pressed_keys[int(self.controls["reset"])]:
            keysToReturn["reset"] = True
        else:
            keysToReturn["reset"] = False

        return keysToReturn

