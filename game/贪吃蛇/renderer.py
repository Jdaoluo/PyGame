"""游戏界面绘制。"""

import pygame

from game.贪吃蛇.config import (
    BLACK,
    BLUE,
    CONTROL_BAR_HEIGHT,
    GREEN,
    GRID_SIZE,
    PLAY_HEIGHT,
    RED,
    WHITE,
    WIDTH,
)


def draw(game):
    """绘制游戏画面和操作按钮。"""
    game.screen.fill(WHITE)

    pygame.draw.rect(
        game.screen,
        RED,
        (
            game.food[0] * GRID_SIZE,
            game.food[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE,
        ),
    )

    for index, position in enumerate(game.snake):
        color = BLUE if index == 0 else GREEN
        pygame.draw.rect(
            game.screen,
            color,
            (
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            ),
        )

    font = pygame.font.SysFont("simhei", 30)
    score_text = font.render(f"分数:{game.score}", True, BLACK)
    game.screen.blit(score_text, (10, 10))

    if game.paused:
        draw_centered_text(game.screen, font, "暂停中", RED)
    elif game.game_over:
        draw_centered_text(game.screen, font, "游戏结束！点击重启游戏", RED)

    button_y = PLAY_HEIGHT + (CONTROL_BAR_HEIGHT - 40) // 2
    game.paused_button = pygame.Rect(WIDTH // 2 - 120, button_y, 100, 40)
    game.restart_button = pygame.Rect(WIDTH // 2 + 20, button_y, 100, 40)

    button_color = (200, 200, 200)
    pygame.draw.rect(game.screen, button_color, game.paused_button)
    paused_text = font.render("继续" if game.paused else "暂停", True, BLACK)
    game.screen.blit(paused_text, (game.paused_button.x + 10, game.paused_button.y + 10))

    pygame.draw.rect(game.screen, button_color, game.restart_button)
    restart_text = font.render("重启", True, BLACK)
    game.screen.blit(restart_text, (game.restart_button.x + 30, game.restart_button.y + 10))

    pygame.display.update()


def draw_centered_text(screen, font, message, color):
    """在屏幕中央绘制提示文字。"""
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, PLAY_HEIGHT // 2))
    screen.blit(text, text_rect)
