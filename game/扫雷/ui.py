"""绘制游戏界面：窗口、按钮、格子、雷、旗子、HUD、结束遮罩。"""

import os
import sys
import pygame

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import settings

pygame.init()


def create_window(width, height):
    """创建指定大小的游戏窗口。"""
    return pygame.display.set_mode((width, height))


def draw_button(screen, rect, text, font_size=30, bg=None, fg=None):
    """在 rect 处绘制一个带边框的按钮。"""
    bg = bg if bg is not None else settings.GRAY
    fg = fg if fg is not None else settings.BLACK
    pygame.draw.rect(screen, bg, rect)
    pygame.draw.rect(screen, settings.BLACK, rect, 2)
    font = pygame.font.Font(settings.FONT_NAME, font_size)
    surf = font.render(text, True, fg)
    screen.blit(surf, surf.get_rect(center=rect.center))


def _draw_hidden(screen, x, y, size):
    """绘制未翻开的格子（带立体凸起感）。"""
    rect = pygame.Rect(x, y, size, size)
    pygame.draw.rect(screen, settings.GRAY, rect)
    # 上、左高光
    pygame.draw.line(screen, settings.WHITE, (x, y), (x + size - 1, y), 2)
    pygame.draw.line(screen, settings.WHITE, (x, y), (x, y + size - 1), 2)
    # 下、右阴影
    pygame.draw.line(screen, settings.DARK_GRAY, (x, y + size - 1), (x + size - 1, y + size - 1), 2)
    pygame.draw.line(screen, settings.DARK_GRAY, (x + size - 1, y), (x + size - 1, y + size - 1), 2)


def _draw_mine(screen, x, y, size):
    """在格子内绘制地雷。"""
    cx, cy = x + size // 2, y + size // 2
    r = size // 4
    pygame.draw.circle(screen, settings.BLACK, (cx, cy), r)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),
                   (-1, -1), (1, 1), (-1, 1), (1, -1)]:
        pygame.draw.line(screen, settings.BLACK, (cx, cy), (cx + dx * r, cy + dy * r), 2)


def _draw_flag(screen, x, y, size):
    """在格子内绘制旗子。"""
    px = x + size // 2
    pygame.draw.line(screen, settings.BLACK, (px, y + size // 4), (px, y + 3 * size // 4), 2)
    pts = [(px, y + size // 4), (px + size // 3, y + size // 3), (px, y + size // 2)]
    pygame.draw.polygon(screen, settings.RED, pts)


def draw_cell(screen, row, col, cell, offset_y):
    """绘制单个格子。cell 为 dict，含 revealed/flagged/mine/adjacent/exploded。"""
    size = settings.CELL_SIZE
    x = col * size
    y = offset_y + row * size
    rect = pygame.Rect(x, y, size, size)

    if cell["revealed"]:
        if cell["mine"]:
            # 翻开的雷：踩到的红色，其余浅灰
            bg = settings.RED if cell.get("exploded") else settings.LIGHT_GRAY
            pygame.draw.rect(screen, bg, rect)
            pygame.draw.rect(screen, settings.DARK_GRAY, rect, 1)
            _draw_mine(screen, x, y, size)
        else:
            pygame.draw.rect(screen, settings.LIGHT_GRAY, rect)
            pygame.draw.rect(screen, settings.DARK_GRAY, rect, 1)
            if cell["adjacent"] > 0:
                color = settings.NUM_COLORS.get(cell["adjacent"], settings.BLACK)
                font = pygame.font.Font(settings.FONT_NAME, int(size * 0.6))
                surf = font.render(str(cell["adjacent"]), True, color)
                screen.blit(surf, surf.get_rect(center=rect.center))
    else:
        _draw_hidden(screen, x, y, size)
        if cell["flagged"]:
            _draw_flag(screen, x, y, size)


def draw_hud(screen, game):
    """绘制顶部信息栏：剩余雷数、重开按钮、计时器。"""
    w = screen.get_width()
    pygame.draw.rect(screen, settings.DARK_GRAY, (0, 0, w, settings.HUD_HEIGHT))
    font = pygame.font.Font(settings.FONT_NAME, 28)

    remaining = game.mines - game.flags_placed
    mine_surf = font.render(f"雷: {remaining:03d}", True, settings.RED)
    screen.blit(mine_surf, (20, 25))

    time_surf = font.render(f"时间: {game.elapsed:03d}", True, settings.RED)
    screen.blit(time_surf, (w - time_surf.get_width() - 20, 25))

    draw_button(screen, game.restart_rect, "重开", font_size=20, bg=settings.YELLOW)


def draw_end_overlay(screen, game):
    """绘制游戏结束遮罩与按钮。"""
    w, h = screen.get_width(), screen.get_height()
    overlay = pygame.Surface((w, h), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(settings.FONT_NAME, 48)
    if game.state == "won":
        text, color = "胜利！", settings.GREEN
    else:
        text, color = "游戏结束", settings.RED
    surf = font.render(text, True, color)
    screen.blit(surf, surf.get_rect(center=(w // 2, h // 2 - 40)))

    draw_button(screen, game.end_restart_rect, "再来一局", font_size=22, bg=settings.YELLOW)
    draw_button(screen, game.end_menu_rect, "返回菜单", font_size=22, bg=settings.GRAY)
