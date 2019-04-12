from abc import *
import pygame
from ui.locals import Direction


# 定义显示抽象类
class Display(metaclass=ABCMeta):  # 参数metaclass=ABCMeta为抽象类的固定写法
    @abstractmethod
    def display(self):
        pass

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


# 定义移动抽象类
class Move(metaclass=ABCMeta):
    @abstractmethod
    def move(self, direction=Direction.NONE):
        pass

    @abstractmethod
    def is_blocked(self, block):
        pass


# 定义阻挡抽象类，其实完全可以当做是一个规范类
class Block(metaclass=ABCMeta):
    pass


# 定义一个排序规范类，即"草"的排序
class Order(metaclass=ABCMeta):
    @abstractmethod
    def get_order(self):
        pass


class AutoMove(Move, ABC):
    pass


class Destroy(metaclass=ABCMeta):
    @abstractmethod
    def is_distroy(self):
        pass

    def display_blast(self):
        return None


# 攻击者
class Attck(ABC):
    @abstractmethod
    def get_power(self):
        pass

    @abstractmethod
    def kill_beaten(self):
        pass

    def is_attacked(self, beaten):
        # 矩形和矩形的碰撞, 当前矩形
        # rect_self = pygame.Rect(self.x, self.y, self.width, self.height)
        # rect_wall = pygame.Rect(beaten.x, beaten.y, beaten.width, beaten.height)
        # return pygame.Rect.colliderect(self.get_rect(), beaten.get_rect())

        collideed = pygame.Rect.colliderect(self.get_rect(), beaten.get_rect())
        if collideed:
            # print("collideed:" + self.get_player_self()+"-----------"+beaten.__str__())
            if self.get_player_self() == beaten.__str__():
                # print("相等了。是自己发射的子弹")
                return False
            else:
                return True

    # 攻击者要返回是那个物体发出攻击的（子弹是谁发的）
    # @abstractmethod
    # def get_player_self(self):
    #     pass


# 被攻击者
class Beaten(ABC):
    @abstractmethod
    def get_hp(self):
        pass

    @abstractmethod
    def receive_beaten(self):
        pass
