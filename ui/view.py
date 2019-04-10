import pygame

from ui.action import Display
from ui.locals import *
from pygame.constants import *


class Iron(Display):#贴墙对象
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.surface = kwargs["surface"]
        self.image = pygame.image.load("img/steels.gif")

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))


class Wall(Display):#普通墙对象
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.surface = kwargs["surface"]
        self.image = pygame.image.load("img/walls.gif")
    def display(self):
        self.surface.blit(self.image, (self.x, self.y))


class TankPlay(Display):#玩家坦克对象
    def __init__(self, **kwargs):
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
        #玩家坦克速度
        self.speed = 2

    def display(self):
        image = None
        if self.direction == Direction.UP:
            image = self.images[0]
        elif self.direction == Direction.DOWN:
            image = self.images[1]
        elif self.direction == Direction.LEFT:
            image = self.images[2]
        elif self.direction == Direction.RIGHT:
            image = self.images[3]
        self.surface.blit(image, (self.x, self.y))

    def move(self,direction):
        #若方向与原来不一致则改变方向，不移动；否则直接移动
        if self.direction != direction:
            self.direction = direction
        else:
            if self.direction == Direction.UP:
                self.y -= self.speed
            elif self.direction == Direction.DOWN:
                self.y += self.speed
            elif self.direction == Direction.LEFT:
                self.x -= self.speed
            elif self.direction == Direction.RIGHT:
                self.x += self.speed

    def fire(self):
        pass
