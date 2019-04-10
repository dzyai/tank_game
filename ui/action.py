from abc import *


# 定义墙体抽象类
class Display(metaclass=ABCMeta):  # 参数metaclass=ABCMeta为抽象类的固定写法
    @abstractmethod
    def display(self):
        pass


# 定义移动抽象类
class Move(metaclass=ABCMeta):
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def is_blocked(self):
        pass


# 定义阻挡抽象类，其实完全可以当做是一个规范类
class Block(metaclass=ABCMeta):
    pass
