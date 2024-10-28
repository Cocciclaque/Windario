import pygame 
import Scripts.levelRenderer as levelRenderer

class WindowAbsolute:

    def __init__(self, position:tuple[int, int], dimension:tuple[int, int], tilesize:int, level:levelRenderer.LevelRenderer, screen:pygame.Surface, offset:tuple[int, int]= (0, 0)):
        self.posX = position[0]
        self.posY = position[1]

        self.offX = 0
        self.offY = 0

        self.sizeX = dimension[0]
        self.sizeY = dimension[1]

        self.dX = dimension[0]*tilesize
        self.dY = dimension[1]*tilesize
        self.tilesize = tilesize

        self.screen = screen

        self.surface:pygame.display = screen.subsurface((self.posX*self.tilesize, self.posY*self.tilesize, self.dX, self.dY))
        self.renderer = levelRenderer.LevelRenderer(self.surface, self.tilesize, level.size_X, level.size_Y, level.dX, level.dY, level.level, level.alias, r"Textures\TextureData")


        self.collisions = []

    def drawWindow(self):
        self.renderer.screen = self.surface
        self.collisions = self.renderer.renderGroundWindowAbsolute(self.posX, self.posY, self.offX, self.offY, self.sizeX, self.sizeY)
        return self.collisions

    def fill(self, color):
        self.surface.fill(color)

    def goto(self, posX, posY):
        self.posX = posX
        self.posY = posY

    def update(self):
            try:
                self.surface = self.screen.subsurface(((self.posX+self.offX)*self.tilesize, (self.offY+self.posY)*self.tilesize, self.dX, self.dY))
            except:
                pass
    def moveLeft(self):
        self.offX -= self.tilesize
        self.posX -= self.tilesize
        self.surface = self.screen.subsurface((self.posX, self.posY, self.dX, self.dY))

    def moveRight(self):
        self.offX += self.tilesize
        self.posX += self.tilesize
        self.surface = self.screen.subsurface((self.posX, self.posY, self.dX, self.dY))

    def moveUp(self):
        self.offY -= self.tilesize
        self.posY -= self.tilesize
        self.surface = self.screen.subsurface((self.posX, self.posY, self.dX, self.dY))

    def moveDown(self):
        self.offY += self.tilesize
        self.posY += self.tilesize
        self.surface = self.screen.subsurface((self.posX, self.posY, self.dX, self.dY))
        
    