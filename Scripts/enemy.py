import pygame
import Scripts.animation as animation
class Enemy:
    
    def __init__(self, screen:pygame.Surface, x:int, y:int, speed:int, pathLength:int, clock:pygame.time.Clock, fps:int=60):
        self.screen:pygame.Surface = screen
        
        self.x:int = x
        self.y:int = y
        
        self.pathLength:int = pathLength
        self.hasMoved:int = 0

        self.lookdir:int = 1

        self.clock:pygame.time.Clock = clock

        self.animation:animation.Animation = animation.Animation(self.screen, r"Textures\TextureData\slime_purple", self.x, self.y, 0.025, None, None, (100, 100), True, "slime", 25, 75)

        self.speed:int = speed

    def update(self):
        self.x += self.speed * self.lookdir
        self.hasMoved += self.speed * self.lookdir

        if self.hasMoved >= self.pathLength or self.hasMoved <= self.pathLength*-1:
            self.lookdir *= -1

        self.animation.x = self.x
        self.animation.lookdir = self.lookdir

        self.animation.animate()

    def isColliding(self, thing:pygame.Rect):
        if thing.colliderect(pygame.Rect(self.animation.x, self.animation.y, 50, 50)):
            return True
        return False