from pygame.constants import K_RETURN
# from pygame.locals import *

current = 0
def setCurrent(value):
    global current
    current = value

def gettCurrent():
    return current

class StartPage:
    def __init__(self,window):
        self.window = window
    def graphic(self):
        self.window.fill((0xff, 0x00, 0x00))
    def keyDown(self,key):
        if key == K_RETURN:
            setCurrent(1)
    def keyPasseding(self,keys):
        pass

class GamePage:
    def __init__(self,window):
        self.window = window
    def graphic(self):
        self.window.fill((0x00, 0x00, 0xff))
    def keyDown(self,key):
        pass
    def keyPasseding(self,keys):
        pass