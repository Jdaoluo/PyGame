"""贪吃蛇游戏状态和主循环。"""

import pygame

from game.贪吃蛇 import events, renderer
from game.贪吃蛇.config import HEIGHT, INITIAL_SPEED, WIDTH
from game.贪吃蛇.logic import create_food, move_snake


class SnakeGame:
    """组合游戏状态、输入、规则和渲染功能。"""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("贪吃蛇")
        self.clock = pygame.time.Clock()
        self.paused_button = pygame.Rect(0, 0, 0, 0)
        self.restart_button = pygame.Rect(0, 0, 0, 0)
        self.reset()

    def reset(self):
        """恢复初始游戏状态。"""
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.direction = (1, 0)
        self.food = create_food(self.snake)
        self.score = 0    
        self.speed = INITIAL_SPEED
        self.paused = False
        self.game_over = False

    def run(self):
        """运行游戏主循环。"""
        while True:
            events.handle_events(self)
            move_snake(self)
            renderer.draw(self)
            self.clock.tick(self.speed)
