from ui.view import *

class GameSurface:
    def __init__(self,surface):
        self.surface = surface

        self.tankPlayer = TankPlay(surface=surface)

    def graphic(self):#是一直执行的
        self.surface.fill((0x00, 0x00, 0x00))
        self.tankPlayer.display()
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