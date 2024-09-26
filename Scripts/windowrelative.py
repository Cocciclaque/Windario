import pygame 
import Scripts.levelRenderer as levelRenderer

class WindowRelative:

    def __init__(self, position:tuple[int, int], dimension:tuple[int, int], level:levelRenderer.LevelRenderer, screen:pygame.Surface, offset:tuple[int, int]= (0, 0)):
        self.posX = position[0]
        self.posY = position[1]

        self.offX = self.posX
        self.offY = self.posY

        self.sizeX = level.size_X
        self.sizeY = level.size_Y

        self.dX = dimension[0]
        self.dY = dimension[1]

        self.screen = screen

        self.surface:pygame.display = screen.subsurface((self.posX, self.posY, self.dX, self.dY))
        self.renderer = levelRenderer.LevelRenderer(self.surface, level.size_X, level.size_Y, level.dX, level.dY, level.level, level.alias)


    def drawWindow(self):
        self.renderer.screen = self.surface
        self.renderer.renderGroundWindow(self.offX, self.offY)

    def fill(self, color):
        self.surface.fill(color)

    def setWindowPos(self, posX, posY):
        self.posX = posX
        self.posY = posY


    def moveLeft(self):
        self.offX -= 50
        self.posX -= 50
        self.surface = self.screen.subsurface((self.posX, self.posY, self.dX, self.dY))

    def moveRight(self):
        self.offX += 50
        self.posX += 50
        self.surface = self.screen.subsurface((self.posX, self.posY, self.dX, self.dY))

    def moveUp(self):
        self.offY -= 50
        self.posY -= 50
        self.surface = self.screen.subsurface((self.posX, self.posY, self.dX, self.dY))

    def moveDown(self):
        self.offY += 50
        self.posY += 50
        self.surface = self.screen.subsurface((self.posX, self.posY, self.dX, self.dY))
        
    