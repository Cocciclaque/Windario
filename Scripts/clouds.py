import pygame
class Cloud:
    
    def __init__(self, imagePath:str, x:int, y:int, speed:int, loopX:int):
        self.imagePath:str = imagePath
        self.image:pygame.Surface = pygame.image.load(imagePath)
        
        self.loopX:int = loopX

        self.x:int = x
        self.y:int = y
        self.speed:int = speed


    
    def update(self):
        self.x += self.speed/3
        if self.x >= self.loopX:
            self.x = -200

    def render(self, screen:pygame.Surface):
        screen.blit(self.image, (self.x, self.y, 200, 200))