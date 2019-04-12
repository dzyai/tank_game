import random

import time
from ui.action import *
from ui.locals import *


class Iron(Display, Block, Beaten):  # 贴墙对象
    def get_hp(self):
        return self.hp

    def receive_beaten(self, power):
        self.hp += 20

    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.surface = kwargs["surface"]
        self.image = pygame.image.load("img/steels.gif")

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hp = 66

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
        return Bullet(x=x, y=y, direction=self.direction, surface=self.surface, flag=self.__str__())


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
        self.flag = kwargs["flag"]
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

    def get_player_self(self):
        return self.flag

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
        # 添加播放图片
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
        self.surface.blit(image, (self.x, self.y))
        self.index += 1

    def is_distroy(self):
        return self.index >= len(self.images)


# 敌方坦克对象
class EnemyPlay(Display, AutoMove, Block, Destroy, Beaten):

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

    def __init__(self, **kwargs):
        # 开始时就有敌军
        self.reset()
        self.hp = 1
        self.surface = kwargs["surface"]
        self.x = kwargs["x"]
        self.y = kwargs["y"]

    def reset(self):
        self.is_distroyed = False
        enemy_i = random.randint(1, 3)
        self.images = [
            pygame.image.load("img/enemy%dU.gif" % enemy_i),
            pygame.image.load("img/enemy%dD.gif" % enemy_i),
            pygame.image.load("img/enemy%dL.gif" % enemy_i),
            pygame.image.load("img/enemy%dR.gif" % enemy_i)
        ]

        self.direction = Direction.UP
        self.speed = 3
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.bad_direction = Direction.NONE

        # 开发发射时间延时
        self.start_time = 0
        self.delay_time = 0.5
        # 移动时间延时
        self.__move_start = 0
        self.__move_delay = 0.03
        self.__move_time = 0
        self.dispositions = []
        # 重置时敌军随机出现
        file = open("map/1.map", "r", encoding="utf-8")
        for row, line in enumerate(file):
            line = line.strip()
            for column, text in enumerate(line):
                x = column * BLOCK
                y = row * BLOCK
                if text == "空":
                    self.dispositions.append((x, y))
        if len(self.dispositions)>0:
            pos = random.randint(0, len(self.dispositions))
            yuanzu = self.dispositions[pos]
            self.x = yuanzu[0]
            self.y = yuanzu[1]
        file.close()

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

    def move(self, d=Direction.NONE):
        """自动移动"""
        now = time.time()
        if now - self.__move_start < self.__move_delay:
            return
        self.__move_start = now

        if self.__move_time >= 60:
            self.__move_time = 0
            # 随机的方向
            self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
            return

        if self.direction == self.bad_direction:
            # 随机的方向
            self.direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT])
            return

        self.__move_time += 1
        # 方向相同
        if self.direction == Direction.UP:
            self.y -= self.speed
            if self.y < 0:
                self.y = 0
        elif self.direction == Direction.DOWN:
            self.y += self.speed
            if self.y > GAME_HEIGHT - self.height:
                self.y = GAME_HEIGHT - self.height
        elif self.direction == Direction.LEFT:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        elif self.direction == Direction.RIGHT:
            self.x += self.speed
            if self.x > GAME_WIDTH - self.width:
                self.x = GAME_WIDTH - self.width

    def is_blocked(self, block):
        # 判断坦克和墙是否碰撞
        # 判断坦克下一步的矩形和现在的墙是否碰撞
        next_x = self.x
        next_y = self.y

        if self.direction == Direction.UP:
            next_y -= self.speed
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

        # 矩形和矩形的碰撞, 当前矩形
        rect_self = pygame.Rect(next_x, next_y, self.width, self.height)
        rect_wall = pygame.Rect(block.x, block.y, block.width, block.height)

        collide = pygame.Rect.colliderect(rect_self, rect_wall)
        if collide:
            # 碰撞了,当的方向是错误的方向
            self.bad_direction = self.direction
            return True
        else:
            # 没有错误方向
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

        return Bullet(x=x, y=y, direction=self.direction, surface=self.surface, flag=self.__str__())


class Home(Display, Beaten, Block, Destroy):

    def __init__(self, **kwargs):
        self.initX = kwargs["x"]  # 老鹰的位置
        self.initY = kwargs["y"]  # 老鹰的位置
        self.surface = kwargs["surface"]

        self.x = self.initX - 25
        self.y = self.initY - 25

        self.wall = pygame.image.load("img/wall.gif")
        self.steel = pygame.image.load("img/steel.gif")
        self.camp = pygame.image.load("img/camp.gif")

        icon_width = 25
        self.locations = [
            (self.x, self.y),
            (self.x + icon_width, self.y),
            (self.x + icon_width * 2, self.y),
            (self.x + icon_width * 3, self.y),
            (self.x, self.y + icon_width),
            (self.x, self.y + icon_width * 2),
            (self.x + icon_width * 3, self.y + icon_width),
            (self.x + icon_width * 3, self.y + icon_width * 2),
        ]

        self.hp = 6

        self.width = self.camp.get_width() + BLOCK
        self.height = self.camp.get_height() + icon_width

    def display(self):
        # 画8个铁
        if self.hp >= 4:
            for loc in self.locations:
                self.surface.blit(self.steel, loc)
        elif self.hp >= 2:
            for loc in self.locations:
                self.surface.blit(self.wall, loc)

        self.surface.blit(self.camp, (self.initX, self.initY))

    def get_hp(self):
        return self.hp

    def receive_beaten(self, power):
        self.hp -= power

        if self.hp < 2:
            self.width = self.camp.get_width()
            self.height = self.camp.get_height()
            self.x = self.initX
            self.y = self.initY

    def is_distroy(self):
        return self.hp <= 0


class InfoEnemyPlay(Display):
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.surface = kwargs["surface"]
        self.enemy_img = pygame.image.load("img/enemy1U.gif")

    def display(self):
        self.surface.blit(self.enemy_img, (self.x, self.y))
