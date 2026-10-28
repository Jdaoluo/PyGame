class Settings:
    """存储游戏中所有设置的类。"""

    def __init__(self):
        """初始化游戏的静态设置。"""
        # 屏幕设置
        self.screen = (1200, 800)
        self.bg_color = (230, 230, 230)
        self.zd_color = (60, 60, 60)

        # 飞船设置
        self.ship_speed = 1.5   
        self.ship_limit = 3  # 飞船的数量   

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = self.zd_color
        self.bullets_allowed = 30  # 限制屏幕上同时出现的子弹数量

        # 外星人设置
        self.fleet_drop_speed = 10

        # 游戏节奏加快的速度
        self.speedup_scale = 1.1
        self.score_scale = 1.5  # 分数提高的速度

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置。"""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        # fleet_direction 为 1 表示向右移，为 -1 表示向左
        self.fleet_direction = 1

        # 记分
        self.alien_points = 50 

    def increase_speed(self):
        """提高速度设置。"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale) 

