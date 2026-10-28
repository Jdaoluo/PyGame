"""游戏设置：颜色、字体、难度、窗口尺寸等配置。"""

import os
import sys
import pygame

# 使本目录下的模块可被直接 import，无论从哪个目录运行
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

pygame.init()

# ---------- 颜色设置 ----------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (192, 192, 192)
YELLOW = (255, 230, 0)
BG_COLOR = (200, 200, 200)

# 经典数字配色 1~8
NUM_COLORS = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128),
}

# ---------- 字体 ----------
FONT_NAME = "C:/Windows/Fonts/simhei.ttf"

# ---------- 棋盘与界面尺寸 ----------
CELL_SIZE = 32          # 每格像素边长
HUD_HEIGHT = 80         # 顶部信息栏高度

# ---------- 难度设置 (行, 列, 雷数) ----------
DIFFICULTIES = {
    "简单": (9, 9, 10),
    "普通": (16, 16, 40),
    "困难": (24, 24, 99),
}

# ---------- 难度选择菜单窗口 ----------
MENU_WIDTH = 400
MENU_HEIGHT = 420


def difficulty_buttons():
    """构建一次难度选择按钮列表，返回 [(rect, 名称, 行, 列, 雷数), ...]。"""
    buttons = []
    btn_w, btn_h = 280, 50
    gap = 20
    n = len(DIFFICULTIES)
    total_h = n * btn_h + (n - 1) * gap
    start_y = 130 + (MENU_HEIGHT - 130 - total_h) // 2
    for i, (diff, (rows, cols, mines)) in enumerate(DIFFICULTIES.items()):
        x = (MENU_WIDTH - btn_w) // 2
        y = start_y + i * (btn_h + gap)
        rect = pygame.Rect(x, y, btn_w, btn_h)
        buttons.append((rect, diff, rows, cols, mines))
    return buttons
