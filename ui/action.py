from abc import *


# 定义显示抽象类
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
    def is_blocked(self,block):
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

class Destroy(ABC):
    @abstractmethod
    def is_distroy(self):
        pass
    pass