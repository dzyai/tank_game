import pygame
from ui.locals import *
class TankPlay:
    def __init__(self,**kwargs):
        self.x = 100
        self.y = 100
        self.images = [
            pygame.image.load("img/p1tankU.gif"),
            pygame.image.load("img/p1tankD.gif"),
            pygame.image.load("img/p1tankL.gif"),
            pygame.image.load("img/p1tankR.gif")
        ]
        self.direction = Direction.UP
        self.surface = kwargs["surface"]
    def display(self):
        image = None
        if self.direction ==  Direction.UP:
            image = self.images[0]
        elif self.direction ==  Direction.DOWN:
            image = self.images[1]
        elif self.direction ==  Direction.LEFT:
            image = self.images[2]
        elif self.direction ==  Direction.RIGHT:
            image = self.images[3]
        self.surface.blit(image,(self.x,self.y))
    def move(self):
        pass
    def fire(self):
        pass