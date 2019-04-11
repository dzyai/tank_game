"""
主窗体
"""
import sys
from ui.page import *

if __name__ == '__main__':
    pygame.init()
    w = WINDOW_WIDTH
    h = WINDOW_HEIGHT
    window = pygame.display.set_mode((w, h))
    screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    # window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("坦克大战")

    start_page = StartPage(screen)
    game_page = GamePage(screen)
    page = None

    while True:

        current_page = gettCurrent()
        if current_page == 0:
            page = start_page
        elif current_page == 1:
            page = game_page

        pygame.transform.scale(screen,(w,h),window)
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
