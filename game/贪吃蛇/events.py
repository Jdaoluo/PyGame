"""键盘、鼠标和窗口事件处理。"""

import sys

import pygame


def handle_events(game):
    """处理游戏输入事件。"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game.game_over:
                if event.key == pygame.K_r:
                    game.reset()
                continue

            if game.paused and event.key != pygame.K_p:
                continue

            if event.key == pygame.K_UP and game.direction != (0, 1):
                game.direction = (0, -1)
            elif event.key == pygame.K_DOWN and game.direction != (0, -1):
                game.direction = (0, 1)
            elif event.key == pygame.K_LEFT and game.direction != (1, 0):
                game.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and game.direction != (-1, 0):
                game.direction = (1, 0)
            elif event.key == pygame.K_p:
                game.paused = not game.paused
            elif event.key == pygame.K_r:
                game.reset()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game.paused_button.collidepoint(event.pos):
                game.paused = not game.paused
            elif game.restart_button.collidepoint(event.pos):
                game.reset()