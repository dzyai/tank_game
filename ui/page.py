from pygame.constants import K_RETURN
# from pygame.locals import *
import pygame
from ui.locals import *
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
        self.window.fill((0xff, 0x00, 0x00))

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

        self.game_surface = GameSurface(self.gameSurface)
        self.info_surface = InfoSurface(self.infoSurface)

    def graphic(self):  # 是一直执行的
        self.window.fill((0x77, 0x77, 0x77))
        self.game_surface.graphic()
        self.window.blit(self.gameSurface, (WINDOW_PADDING, WINDOW_PADDING))
        self.info_surface.graphic()
        self.window.blit(self.infoSurface, (2 * WINDOW_PADDING + GAME_WIDTH, WINDOW_PADDING))

    def keyDown(self, key):
        self.game_surface.keyDown(key)

    def keyPasseding(self, keys):
        self.game_surface.keyPasseding(keys)
