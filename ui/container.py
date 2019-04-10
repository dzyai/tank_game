from ui.view import *

class GameSurface:
    def __init__(self,surface):
        self.surface = surface
        #玩家坦克
        self.tankPlayer = TankPlay(surface=surface)
        #墙
        self.wall1 = Wall(surface=surface, x=200, y=200)
        self.wall2 =Wall(surface=surface,x=300,y=300)
    def graphic(self):#是一直执行的
        self.surface.fill((0x00, 0x00, 0x00))
        self.tankPlayer.display()
        self.wall1.show()
        self.wall2.show()
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