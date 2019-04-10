class GameSurface:
    def __init__(self,surface):
        self.surface = surface
    def graphic(self):
        self.surface.fill((0xff, 0xff, 0x16))
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