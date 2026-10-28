import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """管理飞船的类。"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置。"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()


        # 加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('game\\外星人大战\\images\\ship.bmp')
        self.rect = self.image.get_rect()

        # 将每艘新飞船放在屏幕底部中央
        self.rect.midbottom = self.screen_rect.midbottom

        # 在飞船的属性x和y中存储小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标志（飞船一开始不移动）
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_bottom = False

    def update(self):
        """根据移动标志调整飞船的位置。"""
        if self.moving_right and self.x + self.rect.width < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.x > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.y > 0:
            self.y -= self.settings.ship_speed
        if self.moving_bottom and self.y + self.rect.height < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # 根据self.x和self.y更新rect对象
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self): 
        """在指定位置绘制飞船。"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """让飞船在屏幕上居中。"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

