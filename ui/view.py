import pygame
import time
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


class Wall(Display, Block, Destroy, Beaten):  # 普通墙对象

    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.surface = kwargs["surface"]
        self.image = pygame.image.load("img/walls.gif")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hp = 1
        self.is_distroyed = False

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))

    def get_hp(self):
        return self.hp

    def receive_beaten(self, power):
        self.hp -= power
        if self.hp <= 0:
            self.is_distroyed = True

    def is_distroy(self):
        return self.is_distroyed

    def display_blast(self):
        x = self.x + self.width / 2
        y = self.y + self.height / 2
        return Blast(x=x, y=y, surface=self.surface)


# 玩家坦克对象
class TankPlay(Display, Move):
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

        self.start_time = 0
        self.delay_time = 0.1

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
                if self.y > GAME_HEIGHT - self.height:
                    self.y = GAME_HEIGHT - self.height
                else:
                    self.y += self.speed
            elif self.direction == Direction.LEFT:
                if self.x < 0:
                    self.x = 0
                else:
                    self.x -= self.speed
            elif self.direction == Direction.RIGHT:
                if self.x > GAME_WIDTH - self.width:
                    self.x = GAME_WIDTH - self.width
                else:
                    self.x += self.speed

    # 检测是否发生碰撞,此处仅传入的是砖墙
    def is_blocked(self, block):
        next_x = self.x
        next_y = self.y
        if self.direction == Direction.UP:
            next_y -= self.speed
            # 添加墙体碰撞->"上"，第二种玩家坦克越界处理
            if next_y < 0:
                self.bad_direction = self.direction
                return True
        elif self.direction == Direction.DOWN:
            next_y += self.speed
            if next_y > GAME_HEIGHT - self.height:
                self.bad_direction = self.direction
                return True
        elif self.direction == Direction.LEFT:
            next_x -= self.speed
            if next_x < 0:
                self.bad_direction = self.direction
                return True
        elif self.direction == Direction.RIGHT:
            next_x += self.speed
            if next_x > GAME_WIDTH - self.width:
                self.bad_direction = self.direction
                return True

        pygame_rect = pygame.Rect(next_x, next_y, self.width, self.height)
        wall_rect = pygame.Rect(block.x, block.y, block.width, block.height)
        if pygame.Rect.colliderect(pygame_rect, wall_rect):
            self.bad_direction = self.direction
            return True
        else:
            self.bad_direction = Direction.NONE
            return False

    def fire(self):
        now = time.time()
        if now - self.start_time < self.delay_time:
            return  # 其实是ruturn le None
        self.start_time = now
        # 创建子弹
        x = 0
        y = 0
        if self.direction == Direction.UP:
            x = self.x + self.width / 2
            y = self.y
        elif self.direction == Direction.DOWN:
            x = self.x + self.width / 2
            y = self.y + self.height
        elif self.direction == Direction.LEFT:
            x = self.x
            y = self.y + self.width / 2
        elif self.direction == Direction.RIGHT:
            x = self.x + self.height
            y = self.y + self.width / 2
        return Bullet(x=x, y=y, direction=self.direction, surface=self.surface)


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


class Grass(Display, Order):
    # 抽象方法
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


class Bullet(Display, AutoMove, Destroy, Attck):

    def __init__(self, **kwargs):
        self.surface = kwargs["surface"]
        self.image = pygame.image.load("img/tankmissile.gif")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        x = kwargs["x"]
        y = kwargs["y"]
        self.direction = kwargs["direction"]
        self.y = y
        self.x = x
        self.speed = 4
        if self.direction == Direction.UP:
            self.x = x - self.width / 2
            self.y = y - self.height + 5
        if self.direction == Direction.DOWN:
            self.x = x - self.width / 2
            self.y = y - self.height / 2
        if self.direction == Direction.LEFT:
            self.x = x - self.width / 2
            self.y = y - self.height / 2
        if self.direction == Direction.RIGHT:
            self.x = x - self.width / 2
            self.y = y - self.height / 2

        self.power = 1

        # 是否回收的状态
        self.__is_destroyed = False

    def display(self):
        self.surface.blit(self.image, (self.x, self.y))

    def move(self):
        # 方向相同
        if self.direction == Direction.UP:
            self.y -= self.speed
            if self.y < -self.height:
                # 出屏幕了，回收
                self.__is_destroyed = True
        elif self.direction == Direction.DOWN:
            self.y += self.speed
            if self.y > GAME_HEIGHT:
                # 出屏幕了，回收
                self.__is_destroyed = True
        elif self.direction == Direction.LEFT:
            self.x -= self.speed
            if self.x < -self.width:
                # 出屏幕了，回收
                self.__is_destroyed = True
        elif self.direction == Direction.RIGHT:
            self.x += self.speed
            if self.x > GAME_WIDTH:
                # 出屏幕了，回收
                self.__is_destroyed = True

    def get_power(self):
        return self.power

    def is_blocked(self, block):
        pass

    def is_distroy(self):
        return self.__is_destroyed

    def kill_beaten(self, hp):
        self.power -= hp
        if self.power <= 0:
            self.__is_destroyed = True


# 爆炸对象
class Blast(Display, Destroy):

    def __init__(self, **kwargs):

        self.images = []
        #添加播放图片
        for i in range(1, 33):
            self.images.append(pygame.image.load("img/blast_%d.png" % i))
        self.surface = kwargs["surface"]
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.x = kwargs["x"] - self.width / 2
        self.y = kwargs["y"] - self.height / 2
        self.index = 0

    def display(self):
        if self.index >= len(self.images):
            return
        image = self.images[self.index]
        self.surface.blit(image,(self.x,self.y))
        self.index += 1

    def is_distroy(self):
        return self.index >= len(self.images)


# 敌方坦克对象
class EnemyPlay(Display):
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.images = [
            pygame.image.load("img/enemy1U.gif"),
            pygame.image.load("img/enemy1D.gif"),
            pygame.image.load("img/enemy1L.gif"),
            pygame.image.load("img/enemy1R.gif")
        ]
        self.direction = Direction.UP
        self.surface = kwargs["surface"]
        # 玩家坦克速度
        self.speed = 1

        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.bad_direction = Direction.NONE

        self.start_time = 0
        self.delay_time = 0.1

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
                if self.y > GAME_HEIGHT - self.height:
                    self.y = GAME_HEIGHT - self.height
                else:
                    self.y += self.speed
            elif self.direction == Direction.LEFT:
                if self.x < 0:
                    self.x = 0
                else:
                    self.x -= self.speed
            elif self.direction == Direction.RIGHT:
                if self.x > GAME_WIDTH - self.width:
                    self.x = GAME_WIDTH - self.width
                else:
                    self.x += self.speed

    # 检测是否发生碰撞,此处仅传入的是砖墙
    def is_blocked(self, block):
        next_x = self.x
        next_y = self.y
        if self.direction == Direction.UP:
            next_y -= self.speed
            # 添加墙体碰撞->"上"，第二种玩家坦克越界处理
            if next_y < 0:
                self.bad_direction = self.direction
                return True
        elif self.direction == Direction.DOWN:
            next_y += self.speed
            if next_y > GAME_HEIGHT - self.height:
                self.bad_direction = self.direction
                return True
        elif self.direction == Direction.LEFT:
            next_x -= self.speed
            if next_x < 0:
                self.bad_direction = self.direction
                return True
        elif self.direction == Direction.RIGHT:
            next_x += self.speed
            if next_x > GAME_WIDTH - self.width:
                self.bad_direction = self.direction
                return True

        pygame_rect = pygame.Rect(next_x, next_y, self.width, self.height)
        wall_rect = pygame.Rect(block.x, block.y, block.width, block.height)
        if pygame.Rect.colliderect(pygame_rect, wall_rect):
            self.bad_direction = self.direction
            return True
        else:
            self.bad_direction = Direction.NONE
            return False

    def fire(self):
        now = time.time()
        if now - self.start_time < self.delay_time:
            return  # 其实是ruturn le None
        self.start_time = now
        # 创建子弹
        x = 0
        y = 0
        if self.direction == Direction.UP:
            x = self.x + self.width / 2
            y = self.y
        elif self.direction == Direction.DOWN:
            x = self.x + self.width / 2
            y = self.y + self.height
        elif self.direction == Direction.LEFT:
            x = self.x
            y = self.y + self.width / 2
        elif self.direction == Direction.RIGHT:
            x = self.x + self.height
            y = self.y + self.width / 2
        return Bullet(x=x, y=y, direction=self.direction, surface=self.surface)
