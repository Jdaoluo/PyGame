"""扫雷游戏状态与主循环。"""

import os
import sys
import random
import pygame

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import settings, ui


class Game:
    """管理游戏资源和行为的类。"""

    def __init__(self):
        """初始化游戏。"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.state = "menu"
        self.menu_buttons = settings.difficulty_buttons()

        # 棋盘相关属性，在 new_game 中赋值
        self.board = None
        self.rows = self.cols = self.mines = 0
        self.first_click = True
        self.flags_placed = 0
        self.revealed_count = 0
        self.start_ticks = 0
        self.elapsed = 0
        self.board_top = settings.HUD_HEIGHT
        self.restart_rect = None
        self.end_restart_rect = None
        self.end_menu_rect = None
        self.screen = ui.create_window(settings.MENU_WIDTH, settings.MENU_HEIGHT)

    # ---------- 棋盘初始化 ----------
    def new_game(self, rows, cols, mines):
        """开始一局新游戏。"""
        self.rows, self.cols, self.mines = rows, cols, mines
        self.board = [[{"mine": False, "revealed": False, "flagged": False,
                        "adjacent": 0, "exploded": False} for _ in range(cols)]
                      for _ in range(rows)]
        self.first_click = True
        self.flags_placed = 0
        self.revealed_count = 0
        self.elapsed = 0
        self.state = "playing"

        width = cols * settings.CELL_SIZE
        height = settings.HUD_HEIGHT + rows * settings.CELL_SIZE
        self.screen = ui.create_window(width, height)
        pygame.display.set_caption(f"扫雷 - {rows}×{cols}  {mines}雷")

        self.board_top = settings.HUD_HEIGHT
        self.restart_rect = pygame.Rect(width // 2 - 40, 15, 80, 50)
        self.end_restart_rect = pygame.Rect(width // 2 - 120, height // 2 + 10, 110, 44)
        self.end_menu_rect = pygame.Rect(width // 2 + 10, height // 2 + 10, 110, 44)

    def place_mines(self, safe_r, safe_c):
        """随机布雷，避开首次点击的格子及其 8 邻域，再计算数字。"""
        forbidden = set()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                forbidden.add((safe_r + dr, safe_c + dc))
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)
                     if (r, c) not in forbidden]
        random.shuffle(positions)
        for r, c in positions[:self.mines]:
            self.board[r][c]["mine"] = True
        self.calculate_adjacent()

    def calculate_adjacent(self):
        """计算每个非雷格子周围的雷数。"""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c]["mine"]:
                    continue
                cnt = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.board[nr][nc]["mine"]:
                                cnt += 1
                self.board[r][c]["adjacent"] = cnt

    # ---------- 操作逻辑 ----------
    def reveal(self, r, c):
        """翻开格子，数字为 0 时迭代式洪水填充翻开周围格子。"""
        cell = self.board[r][c]
        if cell["revealed"] or cell["flagged"]:
            return
        if cell["mine"]:
            cell["revealed"] = True
            cell["exploded"] = True
            self.revealed_count += 1
            self.state = "lost"
            self.reveal_all_mines()
            return

        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            cell = self.board[cr][cc]
            if cell["revealed"] or cell["flagged"] or cell["mine"]:
                continue
            cell["revealed"] = True
            self.revealed_count += 1
            if cell["adjacent"] == 0:
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            stack.append((nr, nc))

    def reveal_all_mines(self):
        """失败时展示所有未插旗的雷。"""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c]["mine"] and not self.board[r][c]["flagged"]:
                    self.board[r][c]["revealed"] = True

    def toggle_flag(self, r, c):
        """右键插旗/取消旗。"""
        cell = self.board[r][c]
        if cell["revealed"]:
            return
        cell["flagged"] = not cell["flagged"]
        self.flags_placed += 1 if cell["flagged"] else -1

    def check_win(self):
        """所有非雷格子都被翻开则胜利。"""
        if self.revealed_count == self.rows * self.cols - self.mines:
            self.state = "won"
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.board[r][c]["mine"]:
                        self.board[r][c]["flagged"] = True

    def cell_at(self, pos):
        """由像素坐标得到 (行, 列)，不在棋盘上返回 None。"""
        x, y = pos
        if y < self.board_top:
            return None
        col = x // settings.CELL_SIZE
        row = (y - self.board_top) // settings.CELL_SIZE
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None

    def handle_game_click(self, pos, button):
        """处理游戏中的鼠标点击。"""
        if self.restart_rect and self.restart_rect.collidepoint(pos):
            self.new_game(self.rows, self.cols, self.mines)
            return
        rc = self.cell_at(pos)
        if rc is None:
            return
        r, c = rc
        if button == 1:  # 左键揭开
            if self.first_click:
                self.place_mines(r, c)
                self.first_click = False
                self.start_ticks = pygame.time.get_ticks()
            if not self.board[r][c]["flagged"]:
                self.reveal(r, c)
                if self.state == "playing":
                    self.check_win()
        elif button == 3:  # 右键插旗
            self.toggle_flag(r, c)

    def update_timer(self):
        if self.state == "playing" and not self.first_click:
            self.elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000

    # ---------- 绘制 ----------
    def draw(self):
        self.screen.fill(settings.BG_COLOR)
        ui.draw_hud(self.screen, self)
        for r in range(self.rows):
            for c in range(self.cols):
                ui.draw_cell(self.screen, r, c, self.board[r][c], self.board_top)
        if self.state in ("won", "lost"):
            ui.draw_end_overlay(self.screen, self)

    # ---------- 菜单 ----------
    def run_menu(self):
        """显示难度选择菜单，返回 (名称, 行, 列, 雷数)。"""
        self.screen = ui.create_window(settings.MENU_WIDTH, settings.MENU_HEIGHT)
        pygame.display.set_caption("扫雷 - 难度选择")
        title_font = pygame.font.Font(settings.FONT_NAME, 44)
        sub_font = pygame.font.Font(settings.FONT_NAME, 22)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for rect, diff, rows, cols, mines in self.menu_buttons:
                        if rect.collidepoint(pos):
                            return diff, rows, cols, mines

            self.screen.fill(settings.BG_COLOR)
            title = title_font.render("扫雷", True, settings.BLACK)
            self.screen.blit(title, title.get_rect(center=(settings.MENU_WIDTH // 2, 60)))
            sub = sub_font.render("请选择难度", True, settings.BLACK)
            self.screen.blit(sub, sub.get_rect(center=(settings.MENU_WIDTH // 2, 100)))
            for rect, diff, rows, cols, mines in self.menu_buttons:
                label = f"{diff}  ({rows}×{cols}, {mines}雷)"
                ui.draw_button(self.screen, rect, label, font_size=24)
            pygame.display.flip()
            self.clock.tick(30)

    # ---------- 一局游戏 ----------
    def play(self, diff, rows, cols, mines):
        """运行一局游戏，直到返回菜单。"""
        self.new_game(rows, cols, mines)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.state == "playing":
                        self.handle_game_click(pos, event.button)
                    else:
                        if self.end_restart_rect.collidepoint(pos):
                            self.new_game(rows, cols, mines)
                        elif self.end_menu_rect.collidepoint(pos):
                            return
            self.update_timer()
            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

    # ---------- 主入口 ----------
    def run(self):
        """主循环：菜单 -> 游戏 -> 菜单，反复进行。"""
        while True:
            diff, rows, cols, mines = self.run_menu()
            self.play(diff, rows, cols, mines)


if __name__ == "__main__":
    Game().run()
