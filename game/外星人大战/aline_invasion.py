import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlineInvasion:
    """管理游戏资源和行为的类。"""

    def __init__(self):
        """初始化游戏并创建游戏资源。"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen))
        pygame.display.set_caption("外星人入侵")

        self.stats = GameStats(self)  # 创建一个用于存储游戏统计信息的实例
        self.scoreboard = Scoreboard(self)  # 创建一个用于显示得分的实例

        self.ship = Ship(self) 
        self.bullets = pygame.sprite.Group()  # 创建一个用于存储子弹的编组
        self.aliens = pygame.sprite.Group()  # 创建一个用于存储外星人的编组

        self._create_fleet()  # 创建外星人群
        self.game_active = False  # 游戏刚启动时处于静止状态

        self.play_button = Button(self, "Play")  # 创建一个开始游戏的按钮

    def run_game(self):
        """开始游戏的主循环。"""
        while True:
            self._check_events()

            if self.game_active:  # 只有在游戏处于活动状态时才更新飞船、子弹和外星人
                self.ship.update()  # 更新飞船的位置
                self._update_bullets()  # 更新子弹的位置
                self._update_aliens()  # 更新外星人的位置

            self._update_screen()
            self.clock.tick(60)    # 设置帧率为60帧每秒 

    def _check_events(self):
        """监听键盘和鼠标事件。"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击按钮时开始新游戏。"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()  # 重置游戏设置
            self._start_game()  # 开始新游戏

    def _check_keydown_events(self, event):
        """响应按键按下事件。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = True

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()  # 创建一颗子弹，并将其加入编组bullets中

        elif event.key == pygame.K_p:
            self._start_game()  # 开始新游戏
        
        elif (
            event.key == pygame.K_q
            or event.key == pygame.K_ESCAPE
            ):
            pygame.quit()
            sys.exit()

    def _check_keyup_events(self, event):
        """响应按键松开事件。"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_bottom = False

    def _start_game(self):
        """开始新游戏。"""
        if not self.game_active:
            # 重置游戏设置
            self.settings = Settings()
            self.stats.reset_stats()  # 重置游戏统计信息
            self.scoreboard.prep_score()  # 准备初始得分图像
            self.scoreboard.prep_level()  # 准备初始等级图像
            self.game_active = True  # 游戏处于活动状态

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            self.scoreboard.prep_ships()  # 显示还余下多少艘飞船

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """创建一颗子弹，并将其加入编组bullets中。"""
        if len(self.bullets) < self.settings.bullets_allowed:  # 限制屏幕上同时出现的子弹数量
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置，并删除已消失的子弹。"""
        self.bullets.update()  # 更新子弹位置

        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()  # 检查是否有子弹击中了外星人
        
    def _create_fleet(self):
        """创建外星人群。"""
        # 创建一个外星人，并计算一行可容纳多少个外星人
        alien = Alien(self)
        alien_width, alien_height = alien.rect.width, alien.rect.height

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen[1] - 3 * alien_height):
            while current_x < (self.settings.screen[0] - 2 *alien_width):
                self._create_alien(current_x, current_y)
                current_x += alien_width * 2
            current_x = alien_width
            current_y += alien_height * 2

    def _create_alien(self, x_position, y_position):
        """创建一个外星人并将其放在当前行。"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """更新外星人舰队中外星人的位置。"""
        self._check_fleet_edges()  # 检查是否有外星人到达屏幕边缘
        self.aliens.update()  # 更新外星人位置

        # 检查外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            # print("飞船被撞毁！")
        self._check_aliens_bottom()  # 检查是否有外星人到达了屏幕底端

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施。"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向。"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1  # 改变方向

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端。"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break

    def _ship_hit(self):
        """响应飞船被外星人撞到的事件。"""
        if self.stats.ships_left > 0:
            # 将ships_left减1
            self.stats.ships_left -= 1
            self.scoreboard.prep_ships()  # 更新剩余飞船数量

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底端中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.game_active = False  # 游戏结束
            pygame.mouse.set_visible(True)  # 显示鼠标光标 

    def _check_bullet_alien_collisions(self):
            """检查是否有子弹击中了外星人。"""
            # 如果击中，就删除相应的子弹和外星人
            collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True
            )

            if collisions:
                for aliens in collisions.values():
                    self.stats.score += self.settings.alien_points * len(aliens)
                self.scoreboard.prep_score()  # 更新得分图像
                self.scoreboard.check_high_score()  # 检查是否诞生了新的最高得分
    
            if not self.aliens:  # 如果外星人群被消灭完毕 
                self.bullets.empty()  # 删除现有的子弹
                self._create_fleet()   # 创建一群新的外星人
                self.settings.increase_speed()  # 提高游戏节奏

                # 提高等级
                self.stats.level += 1
                self.scoreboard.prep_level()  # 更新等级图像
        
    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕。"""
        self.screen.fill(self.settings.bg_color)    # 填充背景色

        if not self.game_active:  # 游戏处于静止状态时绘制按钮
            self.play_button.draw_button()
            

        if self.game_active:  # 游戏处于活动状态时绘制飞船、子弹和外星人
            self.scoreboard.show_score()  # 显示得分
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.ship.blitme()    # 绘制飞船
            self.aliens.draw(self.screen)    # 绘制外星人群

        pygame.display.flip()
            

if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlineInvasion()
    ai.run_game()
    