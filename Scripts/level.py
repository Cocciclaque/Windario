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

        self.screen = screen
        
        self.map = map
        self.startX = startpos[0]
        self.startY = startpos[1]

        self.fps = fps

        self.endX = endpos[0]
        self.endY = endpos[1]

        self.clock = clock

        self.renderer:levelRenderer.LevelRenderer = renderer
        self.renderer.endX = self.endX
        self.renderer.endY = self.endY
        # self.renderer.finish = animation.Animation(self.screen, self.renderer.finishdir+"\\"+r"coin", 
        #                                            self.renderer.endX*self.renderer.tilesize,
        #                                            self.renderer.endY*self.renderer.tilesize,
        #                                            0.025, clock,
        #                                            self.fps, (50, 50), True, "coin", 0, 50) 

        self.enemies:list[enemy.Enemy] = [] 

        self.enemiesBasePos:list[int] = []

        self.startingnaw = numAbsoluteWindows
        self.startingnrw = numRelWindows
        self.naw = self.startingnrw
        self.nrw = self.startingnaw
    
        self.font = pygame.font.Font(r"Textures\TextureData\fonts\PixelOperator8-Bold.ttf", 24)

    def render(self):
        self.renderer.renderGround()
        self.renderer.renderFinish()
        self.renderWinNumber()

    def renderWinNumber(self):
        win_abs  = self.font.render(f"Nombre de copié collés restants : {self.naw}.", True, (255, 255, 255))
        self.screen.blit(win_abs, (100, 100))

    def addEnemy(self, x:int, y:int, speed:int, pathLength:int):
        self.enemies.append(enemy.Enemy(self.screen, x, y, speed, pathLength, self.clock, self.fps))
        self.enemiesBasePos.append(x)

    def reload(self):
        for i in range(len(self.enemies)):
            self.enemies[i].x = self.enemiesBasePos[i]
            self.enemies[i].animation.x = self.enemiesBasePos[i]
            self.enemies[i].hasMoved = 0
            self.enemies[i].lookdir = 1
            self.enemies[i].animation.lookdir = 0