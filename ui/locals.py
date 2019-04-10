from enum import Enum

#游戏块
BLOCK = 50
GAME_WIDTH = BLOCK * 13
GAME_HEIGHT = BLOCK * 13
#信息块
INFO_WIDTH = BLOCK * 4
INFO_HEIGHT = GAME_HEIGHT
#窗体
WINDOW_PADDING = 4
WINDOW_WIDTH = GAME_WIDTH + INFO_WIDTH + 3*WINDOW_PADDING
WINDOW_HEIGHT = GAME_HEIGHT + 2*WINDOW_PADDING

#方向枚举列表
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
