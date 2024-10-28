import pygame
import Scripts.clouds as clouds
import os
import random
class Background():
    
    def __init__(self, screen:pygame.Surface, color:pygame.Color, path:str, size:tuple[int, int]):

        self.path:str = path

        self.sizeX:int = size[0]
        self.sizeY:int = size[1]

        self.clouds:list[clouds.Cloud] = []
        self.color:pygame.Color = color
    
        self.screen:pygame.Surface = screen

        self.cloudsImages:list[str] = ["\\".join([self.path, elt]) for elt in os.listdir(self.path)]

        self.fillClouds(random.randint(10, 15))

    def fillClouds(self, number:int):
        for i in range(number):
            self.clouds.append(clouds.Cloud(self.generateCloud(), random.randint(0, self.sizeX), random.randint(0, round(self.sizeY/4)), random.randint(4, 6), self.sizeX+100))

    def generateCloud(self):
        return self.cloudsImages[random.randint(0, len(self.cloudsImages)-1)]


    def renderBackground(self):
        self.screen.fill(self.color)

        self.renderClouds()

    
    def renderClouds(self):
        for cloud in self.clouds:
            cloud.update()
            cloud.render(self.screen)


if __name__ == "__main__":
    bg = Background(10, 10, r"Textures\TextureData\clouds")
    bg.fillClouds(10)
    print(bg.clouds)