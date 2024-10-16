import pygame
import os

class Animation:

    def __init__(self, screen:pygame.Surface, spriteDir:str, x:int, y:int, frameDuration:float, clock:pygame.time.Clock, fps:int, size:tuple[int, int], loop:bool, name="fill"):
        self.screen = screen
        self.spriteDir = spriteDir
        self.value = 0

        self.frame_duration = frameDuration
        self.frame_time = 0

        self.fps = fps

        self.lookdir = 1

        self.clock = clock

        self.x = x
        self.y = y

        self.name = name

        self.size_X = size[0]
        self.size_Y = size[1]

        self.currentSprite = pygame.image.load(self.spriteDir+r"\\"+os.listdir(self.spriteDir)[0])
        self.currentSprite = pygame.transform.scale(self.currentSprite, (self.size_X, self.size_Y))

        self.active = True
        self.finished = False

        self.loopable = loop

    def toggleActive(self):
        if self.active == False:
            self.active = True

    def animate(self):
        print("test")
        if self.frame_time>self.frame_duration:
            
            self.frame_time = 0


            spritesAddress = []
            for elt in os.listdir(self.spriteDir):
                spritesAddress.append(self.spriteDir +r"\\" + elt)

            sprites = []


            if self.lookdir == 1:
                for elt in spritesAddress:
                    sprites.append(pygame.transform.scale(pygame.image.load(elt).convert_alpha(), (self.size_X, self.size_Y)))
            else:
                for elt in spritesAddress:
                    sprites.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(elt).convert_alpha(), (self.size_X, self.size_Y)), True, False))

            if self.value >= len(sprites):
                self.value = 0
                
                if self.loopable == False:
                    self.finished = True
            
            self.currentSprite = sprites[self.value]

            self.value += 1
        
        if self.active == True:
            self.screen.blit(self.currentSprite, (self.x, self.y))
        
        self.tick()

    def tick(self):
        dt = self.clock.tick(self.fps)/1000
        self.frame_time += dt

