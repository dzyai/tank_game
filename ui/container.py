from ui.view import *
from pygame.constants import *
from ui.action import *


class GameSurface:
    def __init__(self, surface):
        self.surface = surface
        self.views = []
        # 玩家坦克
        # self.tankPlayer = TankPlay(surface=surface)
        # #墙
        # self.wall1 = Wall(surface=surface, x=200, y=200)
        # self.wall2 = Wall(surface=surface,x=300,y=300)
        # # 铁
        # self.iron = Iron(surface=surface, x=400, y=400)
        # self.views.append(self.tankPlayer)
        # self.views.append(self.wall1)
        # self.views.append(self.wall2)dd
        # self.views.append(self.iron)
        file = open("map/1.map", "r", encoding="utf-8")
        for row, line in enumerate(file):
            line = line.strip()
            for column, text in enumerate(line):
                x = column * BLOCK
                y = row * BLOCK
                if text == "主":
                    self.tankPlayer = TankPlay(surface=surface, x=x, y=y)
                    self.views.append(self.tankPlayer)
                elif text == "砖":
                    self.wall = Wall(surface=surface, x=x, y=y)
                    self.views.append(self.wall)
                elif text == "铁":
                    self.iron = Iron(surface=surface, x=x, y=y)
                    self.views.append(self.iron)
                elif text == "水":
                    self.iron = Water(surface=surface, x=x, y=y)
                    self.views.append(self.iron)
                elif text == "草":
                    self.iron = Grass(surface=surface, x=x, y=y)
                    self.views.append(self.iron)
        file.close()

    # 函数sort会根据每个元素对象的返回数值进行排序，“草”的返回值为100，其他元素均为0
    def __sort(self, view):
        return view.get_order() if isinstance(view, Order) else 0

    def graphic(self):  # 是一直执行的
        self.surface.fill((0x00, 0x00, 0x00))
        # self.tankPlayer.display()
        # self.wall1.show()
        # self.wall2.show()
        # self.iron.show()
        # 遍历显示游戏Surface页面物体
        for view in self.views:
            view.display()
        # 遍历检测玩家坦克与碰撞物
        # for view in self.views:
        #     if isinstance(view,Wall) or isinstance(view,Iron):#如果是墙体,则进行检测，其他物体不进行检测
        #         blocked = self.tankPlayer.isBlocked(view)
        #         if blocked:
        #             break

        for move in self.views:
            if isinstance(move, Move):  # 如果是移动的物体（此处指玩家坦克），再遍历所有物体
                for block in self.views:
                    # 找出所有可阻塞移动的物体
                    if isinstance(block, Block):  # 如果是障碍物,就判断碰撞
                        if move.is_blocked(block):
                            '''
                            移动的物体被阻塞的物体挡住了,就break，更改错误方向后停止遍历。
                            若不加break，当遍历到其他物体时，错误方向就会被清除
                            '''
                            break

        # 第一种排序：对列表进行排序，排序的标准
        # self.views.sort(key=lambda view: view.get_order() if isinstance(view, Order) else 0)#view为views中的单元素
        # 第二种排序：使用系统函数的排序
        # self.views = sorted(self.views,key=self.__sort)
        # 第三种排序：列表自身的排序。和第一种lambda 相类似
        self.views.sort(key=self.__sort)

        # 添加自动移动物体 并 移动
        for automove in self.views:
            if isinstance(automove, AutoMove):
                automove.move()

        # 是否是销毁物体
        for destroy_view in self.views:
            if isinstance(destroy_view, Destroy) and destroy_view.is_distroy():
                self.views.remove(destroy_view)

        #子弹与其他物体
        # for bullet in self.views:
        #     if isinstance(bullet, Bullet):
        #         for wall in self.views:
        #             # 找出可以被销毁的物体，此处指wall墙
        #             if isinstance(wall, Wall) and bullet.is_blocked(wall):
        #                     power = bullet.get_power()
        #                     hp = wall.get_hp()
        #                     bullet.kill_beaten(hp)
        #                     wall.receive_beaten(power)
        #                     break

        # 攻击者与被攻击者
        for attack in self.views:
            if isinstance(attack, Attck):
                for beaten in self.views:
                    # 找出可以被销毁的物体，此处指wall墙
                    if isinstance(beaten, Beaten):
                        if attack.is_attacked(beaten):
                            power = attack.get_power()
                            hp = beaten.get_hp()
                            attack.kill_beaten(hp)
                            beaten.receive_beaten(power)
                            break

    def keyDown(self, key):
        # 按下事件
        pass

    def keyPasseding(self, keys):
        # 长按事件
        if keys[K_a] or keys[K_LEFT]:
            self.tankPlayer.move(Direction.LEFT)
        if keys[K_d] or keys[K_RIGHT]:
            self.tankPlayer.move(Direction.RIGHT)
        if keys[K_w] or keys[K_UP]:
            self.tankPlayer.move(Direction.UP)
        if keys[K_s] or keys[K_DOWN]:
            self.tankPlayer.move(Direction.DOWN)
        if keys[K_RETURN] or keys[K_SPACE]:
            # self.views.append(self.tankPlayer.fire())#也可直接添加
            fire = self.tankPlayer.fire()
            if fire != None:
                self.__add_view(fire)


    def __add_view(self, view):
        self.views.append(view)


class InfoSurface:
    def __init__(self, surface):
        self.surface = surface

    def graphic(self):
        self.surface.fill((0x16, 0x77, 0xff))

    def keyDown(self):
        pass

    def keyPasseding(self):
        pass
