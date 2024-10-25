import pygame
class LevelRenderer:

    def __init__(self, screen:pygame.display, tilesize:int, size_X:int, size_Y:int, dimension_X:int, dimension_Y:int, level:list[list[int]], alias:list[str]):
        self.screen = screen
        self.size_X = size_X
        self.size_Y = size_Y
        self.dX = dimension_X
        self.dY = dimension_Y
        self.level = level

        self.alias = alias

        self.tilesize = tilesize

        self.offset_X = 0
        self.offset_Y = 0

        self.tilesize = self.dY/self.size_Y

        self.collisions = []

    def renderGround(self):

        collisions = []

        for X in range(len(self.level[0])):
            for Y in range(len(self.level)):
                if self.level[Y][X] != "0":

                    collisions.append(pygame.Rect(X*self.tilesize, Y*self.tilesize, self.tilesize, self.tilesize))

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
    
    def renderGroundWindowAbsolute(self, offsetX, offsetY, sizeX, sizeY):
        
        collisions = []

        for X in range(int(offsetX), int(offsetX)+sizeX):
            for Y in range(int(offsetY), int(offsetY)+sizeY):
                if self.level[Y][X] != "0":
                    collisions.append(pygame.Rect(X*self.tilesize, Y*self.tilesize, self.tilesize, self.tilesize))
                    sprite = pygame.image.load(self.alias[self.level[Y][X]]).convert_alpha()

                    spriteblit = pygame.transform.scale(sprite, (self.tilesize, self.tilesize))
                    
                    self.screen.blit(spriteblit, ((X*self.tilesize), (Y*self.tilesize)))
        return collisions

