"""贪吃蛇的游戏规则。"""

import random

from game.贪吃蛇.config import GRID_SIZE, INITIAL_SPEED, PLAY_HEIGHT, WIDTH


def create_food(snake):
    """随机生成一个不在蛇身上的食物坐标。"""
    while True:
        position = (
            random.randint(1, WIDTH // GRID_SIZE - 2),
            random.randint(1, PLAY_HEIGHT // GRID_SIZE - 2),
        )
        if position not in snake:
            return position


def move_snake(game):
    """移动蛇，并处理边界、自撞和吃食物。"""
    if game.paused or game.game_over:
        return

    head = (
        game.snake[0][0] + game.direction[0],
        game.snake[0][1] + game.direction[1],
    )

    hit_boundary = (
        head[0] < 0
        or head[0] >= WIDTH // GRID_SIZE
        or head[1] < 0
        or head[1] >= PLAY_HEIGHT // GRID_SIZE
    )
    if hit_boundary or head in game.snake:
        game.game_over = True
        return

    game.snake.insert(0, head)
    if head == game.food:
        game.score += 10
        game.food = create_food(game.snake)
        game.speed = INITIAL_SPEED + game.score // 100
    else:
        game.snake.pop()
