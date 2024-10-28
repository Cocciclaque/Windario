import pygame 
import Scripts.levelRenderer as levelRenderer

class WindowRelative:

    def __init__(self, position:tuple[int, int], dimension:tuple[int, int], tilesize:int, level:levelRenderer.LevelRenderer, screen:pygame.Surface, offset:tuple[int, int]= (0, 0)):
        self.posX:int = position[0]
        self.posY:int = position[1]

        self.offX:int = self.posX
        self.offY:int = self.posY

        self.sizeX:int = dimension[0]
        self.sizeY:int = dimension[1]

        self.dX:int = dimension[0]*tilesize
        self.dY:int = dimension[1]*tilesize

        self.tilesize:int = tilesize

        self.screen:pygame.Surface = screen

        self.surface:pygame.display = screen.subsurface((self.posX*self.tilesize, self.posY*self.tilesize, self.dX, self.dY))
        self.renderer = levelRenderer.LevelRenderer(self.surface, self.tilesize, level.size_X, level.size_Y, level.dX, level.dY, level.level, level.alias, r"Textures\TextureData")

        self.collisions:list[pygame.Rect] = []

    def drawWindow(self):
        self.renderer.screen = self.surface
        self.collisions = self.renderer.renderGroundWindowRelative(self.posX, self.posY, self.sizeX, self.sizeY)
        
    def update(self):
            try:
                self.surface = self.screen.subsurface((self.posX*self.tilesize, self.posY*self.tilesize, self.dX, self.dY))
            except:
                pass

    def fill(self, color):
        self.surface.fill(color)

    def setWindowPos(self, posX, posY):
        self.posX = posX
        self.posY = posY


    def moveLeft(self):
        self.offX -= self.tilesize
        self.posX -= self.tilesize
        if self.posX < 0:
            self.posX += self.tilesize
            self.offX += self.tilesize
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
        
    