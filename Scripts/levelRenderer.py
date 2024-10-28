import pygame
import Scripts.animation as animation
class LevelRenderer:

    def __init__(self, screen:pygame.Surface, tilesize:int, size_X:int, size_Y:int, dimension_X:int, dimension_Y:int, level:list[list[int]], alias:list[str], finishdir:str):
        self.screen:pygame.Surface = screen
        self.size_X:int = size_X
        self.size_Y:int = size_Y
        self.dX:int = dimension_X
        self.dY:int = dimension_Y
        self.level:list[list[int]] = level

        self.alias:list[str] = alias

        self.endX:int = 0
        self.endY:int = 0

        self.finishImage:pygame.Surface = pygame.transform.scale(pygame.image.load(r"Textures\flag.png").convert_alpha(), (50, 50))

        self.tilesize:int = tilesize

        self.offset_X:int = 0
        self.offset_Y:int = 0

        self.tilesize:int = self.dY/self.size_Y

        self.collisions:list[pygame.Rect] = []

    def renderFinish(self):
        self.screen.blit(self.finishImage, (self.endX * self.tilesize, self.endY * self.tilesize, 10, 10))

    def renderGround(self):

        collisions = []

        for X in range(len(self.level[0])):
            for Y in range(len(self.level)):
                if self.level[Y][X] != "0":

                    if self.level[Y][X] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                        collisions.append(pygame.Rect(X*self.tilesize, Y*self.tilesize, self.tilesize, self.tilesize))
                    else:
                        collisions.append(pygame.Rect(X*self.tilesize, Y*self.tilesize, self.tilesize, self.tilesize/2))
                    if self.level[Y][X] != "%":
                        sprite = pygame.transform.scale(pygame.image.load(self.alias[self.level[Y][X]]).convert_alpha(), (self.tilesize, self.tilesize))
                        self.screen.blit(sprite, (X*self.tilesize, Y*self.tilesize))
        
        self.collisions = collisions

    def renderGroundWindowRelative(self, offsetX, offsetY, sizeX, sizeY):
        
        collisions = []

        for X in range(int(offsetX), int(offsetX)+sizeX):
            for Y in range(int(offsetY), int(offsetY)+sizeY):
                if self.level[Y][X] != "0":
                    collisions.append(pygame.Rect(X*self.tilesize, Y*self.tilesize, self.tilesize, self.tilesize))
                    sprite = pygame.image.load(self.alias[self.level[Y][X]]).convert_alpha()

                    spriteblit = pygame.transform.scale(sprite, (self.tilesize, self.tilesize))
                    
                    self.screen.blit(spriteblit, ((X*self.tilesize)-(offsetX*self.tilesize), (Y*self.tilesize)-(offsetY*self.tilesize)))

        return collisions
    
    def renderGroundWindowAbsolute(self, initialposX, initialposY, offsetX, offsetY, sizeX, sizeY):


        collisions = []


        for X in range(int(initialposX), int(initialposX)+sizeX):
            for Y in range(int(initialposY), int(initialposY)+sizeY):
                if self.level[Y][X] != "0" and self.level[Y][X] != "N":
                    collisions.append(pygame.Rect(((X+offsetX)*self.tilesize), ((Y+offsetY)*self.tilesize), self.tilesize, self.tilesize))
                    sprite = pygame.image.load(self.alias[self.level[Y][X]]).convert_alpha()

                    spriteblit = pygame.transform.scale(sprite, (self.tilesize, self.tilesize))
                    self.screen.blit(spriteblit, (((X-initialposX)*self.tilesize), ((Y-initialposY)*self.tilesize)))
        return collisions

