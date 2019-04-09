"""
主窗体
"""
import sys
import pygame
from pygame.locals import *
from ui.locals import *
from ui.page import *

if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("坦克大战")

    start_page = StartPage(window)
    game_page = GamePage(window)
    page = None
    while True:

        current_page = gettCurrent()
        if current_page == 0:
            page = start_page
        elif current_page == 1:
            page = game_page

        #渲染窗体
        page.graphic()
        pygame.display.flip()

        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            if event.type == KEYDOWN:
                page.keyDown(event.key)

        #传递长按键事件
        keys = pygame.key.get_pressed()
        page.keyPasseding(keys)
