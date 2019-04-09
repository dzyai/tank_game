"""
主窗体
"""
import sys
import pygame

from ui.locals import *

if __name__ == '__main__':
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("坦克大战")
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type== pygame.QUIT:
                sys.exit(0)

