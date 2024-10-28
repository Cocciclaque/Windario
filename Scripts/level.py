import pygame
import Scripts.levelRenderer as levelRenderer
import Scripts.animation as animation
import Scripts.enemy as enemy
class Level:

    def __init__(self, screen:pygame.display, map:str, 
                 startpos:tuple[int, int], endpos:tuple[int, int], 
                 numAbsoluteWindows:int, 
                 numRelWindows:int, renderer:levelRenderer.LevelRenderer, 
                 clock:pygame.time.Clock, config:str,
                 fps:int=60):

        self.screen:pygame.Surface = screen
        
        self.map:str = map
        self.startX:int = startpos[0]
        self.startY:int = startpos[1]

        self.fps:int = fps

        self.endX:int = endpos[0]
        self.endY:int = endpos[1]

        self.clock:pygame.time.Clock = clock

        self.renderer:levelRenderer.LevelRenderer = renderer
        self.renderer.endX:int = self.endX
        self.renderer.endY:int = self.endY

        self.enemies:list[enemy.Enemy] = [] 

        self.enemiesBasePos:list[int] = []

        self.startingnaw:int = numAbsoluteWindows
        self.startingnrw:int = numRelWindows
        self.naw:int = self.startingnrw
        self.nrw:int = self.startingnaw
    
        self.font:pygame.font.Font = pygame.font.Font(r"Textures\TextureData\fonts\PixelOperator8-Bold.ttf", 24)
        self.textFont:pygame.font.Font = pygame.font.Font(r"Textures\TextureData\fonts\PixelOperator8-Bold.ttf", 18)

        self.text:list[pygame.font.Font] = []
        self.textPos:list[int, int] = []

    def render(self):
        self.renderer.renderGround()
        self.renderer.renderFinish()
        self.renderText()
        self.renderWinNumber()

    def renderText(self):
        for i in range(len(self.text)):
            self.screen.blit(self.text[i], (self.textPos[i][0], self.textPos[i][1]))

    def renderWinNumber(self):
        win_abs  = self.font.render(f"Nombre de copié collés restants : {self.naw}.", True, (255, 255, 255))
        self.screen.blit(win_abs, (100, 100))

    def addEnemy(self, x:int, y:int, speed:int, pathLength:int):
        self.enemies.append(enemy.Enemy(self.screen, x, y, speed, pathLength, self.clock, self.fps))
        self.enemiesBasePos.append(x)

    def addText(self, x:int, y:int, text:str):
        self.text.append(self.textFont.render(text, True, (255, 255, 255)))
        self.textPos.append([x, y])

    def reload(self):
        for i in range(len(self.enemies)):
            self.enemies[i].x = self.enemiesBasePos[i]
            self.enemies[i].animation.x = self.enemiesBasePos[i]
            self.enemies[i].hasMoved = 0
            self.enemies[i].lookdir = 1
            self.enemies[i].animation.lookdir = 0