#定义墙体抽象类
from abc import *

class Display(metaclass=ABCMeta):# 参数metaclass=ABCMeta为抽象类的固定写法
    @abstractmethod
    def display(self):
        pass