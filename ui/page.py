from ui.container import *

current = 1


def setCurrent(value):
    global current
    current = value


def gettCurrent():
    return current


class StartPage:
    def __init__(self, window):
        self.window = window

    def graphic(self):
        self.window.fill((0x3e, 0x3e, 0xff))

    def keyDown(self, key):
        if key == K_RETURN:
            setCurrent(1)

    def keyPasseding(self, keys):
        pass


class GamePage:
    def __init__(self, window):
        self.window = window
        self.gameSurface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.infoSurface = pygame.Surface((INFO_WIDTH, INFO_HEIGHT))

        self.game_surface = GameSurface(self.gameSurface,self)
        self.info_surface = InfoSurface(self.infoSurface, self)

        self.SURPLUS_ENEMY = 20

    def graphic(self):  # 是一直执行的
        self.window.fill((0x50, 0x50, 0x50))
        self.game_surface.graphic()
        self.window.blit(self.gameSurface, (WINDOW_PADDING, WINDOW_PADDING))
        self.info_surface.graphic()
        self.window.blit(self.infoSurface, (2 * WINDOW_PADDING + GAME_WIDTH, WINDOW_PADDING))

    def get_surplus_enemy(self):
        # if self.SURPLUS_ENEMY == None:
        #     return 20
        # else:
        #     return self.SURPLUS_ENEMY
        try:
            return self.SURPLUS_ENEMY
        except Exception as e:
            return 20

    def set_surplus_enemy(self):
        self.SURPLUS_ENEMY -= 1
        self.info_surface.__init__(self.infoSurface, self)
        if self.SURPLUS_ENEMY < 0 :
            self.SURPLUS_ENEMY = 0

    def keyDown(self, key):
        self.game_surface.keyDown(key)

    def keyPasseding(self, keys):
        self.game_surface.keyPasseding(keys)
