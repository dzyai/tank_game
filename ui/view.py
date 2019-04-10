import pygame

from ui.action import *
from ui.locals import *


class Iron(Display, Block):  # 贴墙对象
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.surface = kwargs["surface"]
        self.image = pygame.image.load("img/steels.gif")

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))


class Wall(Display, Block):  # 普通墙对象
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.surface = kwargs["surface"]
        self.image = pygame.image.load("img/walls.gif")
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))


class TankPlay(Display, Move):  # 玩家坦克对象
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.images = [
            pygame.image.load("img/p1tankU.gif"),
            pygame.image.load("img/p1tankD.gif"),
            pygame.image.load("img/p1tankL.gif"),
            pygame.image.load("img/p1tankR.gif")
        ]
        self.direction = Direction.UP
        self.surface = kwargs["surface"]
        # 玩家坦克速度
        self.speed = 1

        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()

        self.bad_direction = Direction.NONE

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

    def move(self, direction):
        if self.bad_direction == direction:
            return

        # 若方向与原来不一致则改变方向，不移动；否则直接移动
        if self.direction != direction:
            self.direction = direction
        else:
            if self.direction == Direction.UP:
                if self.y < 0:
                    self.y = 0
                else:
                    self.y -= self.speed
            elif self.direction == Direction.DOWN:
                if self.y > GAME_HEIGHT-self.height:
                    self.y = GAME_HEIGHT-self.height
                else:
                    self.y += self.speed
            elif self.direction == Direction.LEFT:
                if self.x < 0:
                    self.x = 0
                else:
                    self.x -= self.speed
            elif self.direction == Direction.RIGHT:
                if self.x > GAME_WIDTH-self.width:
                    self.x = GAME_WIDTH-self.width
                else:
                    self.x += self.speed

    # 检测是否发生碰撞,此处仅传入的是砖墙
    def is_blocked(self, view):
        next_x = self.x
        next_y = self.y
        if self.direction == Direction.UP:
            next_y -= self.speed
        elif self.direction == Direction.DOWN:
            next_y += self.speed
        elif self.direction == Direction.LEFT:
            next_x -= self.speed
        elif self.direction == Direction.RIGHT:
            next_x += self.speed

        pygame_rect = pygame.Rect(next_x, next_y, self.width, self.height)
        wall_rect = pygame.Rect(view.x, view.y, view.width, view.height)
        if pygame.Rect.colliderect(pygame_rect, wall_rect):
            self.bad_direction = self.direction
            return True
        else:
            self.bad_direction = Direction.NONE
            return False

    def fire(self):
        pass


class Water(Display, Block):
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.surface = kwargs["surface"]
        self.image = pygame.image.load("img/water.gif")
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))


class Grass(Display,Order):
    #抽象方法
    def get_order(self):
        return 100

    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.surface = kwargs["surface"]
        self.image = pygame.image.load("img/grass.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))
