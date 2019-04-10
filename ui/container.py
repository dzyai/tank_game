from ui.view import *

class GameSurface:
    def __init__(self,surface):
        self.surface = surface
        self.views = []
        #玩家坦克
        self.tankPlayer = TankPlay(surface=surface)
        #墙
        self.wall1 = Wall(surface=surface, x=200, y=200)
        self.wall2 = Wall(surface=surface,x=300,y=300)
        # 铁
        self.iron = Iron(surface=surface, x=400, y=400)
        self.views.append(self.tankPlayer)
        self.views.append(self.wall1)
        self.views.append(self.wall2)
        self.views.append(self.iron)
    def graphic(self):#是一直执行的
        self.surface.fill((0x00, 0x00, 0x00))
        # self.tankPlayer.display()
        # self.wall1.show()
        # self.wall2.show()
        # self.iron.show()

        #遍历显示游戏Surface页面物体
        for view in self.views:
            view.display()

    def keyDown(self):
        pass
    def keyPasseding(self):
        pass
class InfoSurface:
    def __init__(self,surface):
        self.surface = surface
    def graphic(self):
        self.surface.fill((0x16, 0x77, 0xff))
    def keyDown(self):
        pass
    def keyPasseding(self):
        pass