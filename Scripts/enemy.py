import pygame
import Scripts.animation as animation
class Enemy:
    
    def __init__(self, screen:pygame.Surface, x:int, y:int, speed:int, pathLength:int, clock:pygame.time.Clock, fps:int=60):
        self.screen = screen
        
        self.x = x
        self.y = y
        
        self.pathLength = pathLength
        self.hasMoved = 0

        self.lookdir = 1

        self.clock = clock

        self.animation = animation.Animation(self.screen, r"Textures\TextureData\slime_purple", self.x, self.y, 0.025, None, None, (100, 100), True, "slime", 25, 75)

        self.speed = speed

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