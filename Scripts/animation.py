import pygame
import os

class Animation:

    def __init__(self, screen:pygame.Surface, spriteDir:str, x:int, y:int, frameDuration:float, clock:pygame.time.Clock, fps:int, size:tuple[int, int], loop:bool, name="fill", offsetPos:int=0, offsetSize:int=0):
        self.screen:pygame.Surface = screen
        self.spriteDir:str = spriteDir
        self.value:int = 0

        self.frame_duration:float = frameDuration
        self.frame_time:float = 0

        self.fps:int = fps

        self.lookdir:int = 1

        self.clock:pygame.time.Clock = clock

        self.spriteOffsetPos:int = offsetPos
        self.spriteOffsetSize:int = offsetSize


        self.x:int = x
        self.y:int = y

        self.name:str = name

        self.size_X:int = size[0]
        self.size_Y:int = size[1]

        self.sprites:list[pygame.Surface] = [pygame.transform.scale(pygame.image.load(self.spriteDir+r"\\"+elt).convert_alpha(), (self.size_X, self.size_Y)) for elt in os.listdir(self.spriteDir)]

        self.firstSprite:int = 0
        self.currentSprite:pygame.Surface = self.sprites[self.firstSprite]

        self.active:bool = True
        self.finished:bool = False

        self.loopable:bool = loop

    def resetAnimation(self):
        self.currentSprite = self.sprites[self.firstSprite]
        self.value = 0
        self.frame_time = 0

    def toggleActive(self):
        if self.active == False:
            self.active = True

    def animate(self):
            
        if self.frame_time>self.frame_duration:
            self.frame_time = 0
            self.value += 1
            if self.value == len(self.sprites) and self.loopable == True:
                self.value = 0
            elif self.value == len(self.sprites) and self.loopable == False:
                self.value = len(self.sprites)-1
                self.finished = True
        
        if self.active == True:
            if self.lookdir == -1:
                self.currentSprite = pygame.transform.flip(self.currentSprite, True, False)
            self.screen.blit(self.currentSprite, (self.x, self.y), (self.spriteOffsetPos, self.spriteOffsetPos, self.spriteOffsetSize, self.spriteOffsetSize))
        
            self.currentSprite = self.sprites[self.firstSprite + self.value]
            
        if self.spriteDir != r"Textures\TextureData\coin" and self.spriteDir != r"Textures\TextureData\slime_purple":
            self.tick()

    def tick(self):
        dt = self.clock.tick(self.fps)/1000
        self.frame_time += dt

