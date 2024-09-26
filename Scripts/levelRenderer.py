import pygame
class LevelRenderer:

    def __init__(self, screen:pygame.display, size_X:int, size_Y:int, dimension_X:int, dimension_Y:int, level:list[list[int]], alias:list[str]):
        self.screen = screen
        self.size_X = size_X
        self.size_Y = size_Y
        self.dX = dimension_X
        self.dY = dimension_Y
        self.level = level

        self.alias = alias

        self.tilesize = round(self.dY/self.size_Y)

        self.offset_X = 0
        self.offset_Y = 0

    def renderGround(self):

        for X in range(len(self.level[0])):
            for Y in range(len(self.level)):
                if self.level[Y][X] != "0":

                    sprite = pygame.transform.scale(pygame.image.load(self.alias[self.level[Y][X]]).convert_alpha(), (self.tilesize, self.tilesize))
                    self.screen.blit(sprite, (X*self.tilesize, Y*self.tilesize))


    def renderGroundWindow(self, offsetX, offsetY):
        
        for X in range(len(self.level[0])):
            for Y in range(len(self.level)):
                if self.level[Y][X] != "0":
                    sprite = pygame.image.load(self.alias[self.level[Y][X]]).convert_alpha()

                    spriteblit = pygame.transform.scale(sprite, (self.tilesize, self.tilesize))
                    
                    self.screen.blit(spriteblit, ((X*self.tilesize)-offsetX, (Y*self.tilesize)-offsetY))


