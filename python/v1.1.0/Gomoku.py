import pygame
import sys
import tkinter
import os
from tkinter import messagebox

root = tkinter.Tk()
root.withdraw()

# 打包兼容路径
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS  # PyInstaller 打包后的临时目录
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class game():
    def __init__(self, screen_long=800):
        pygame.init()
        pygame.display.set_caption("五子棋（beihai）")
        self.margin_ratio = 1 / 20
        self.matrix = [[0] * 15 for _ in range(15)]

        # 初始化窗口先设置大小
        self.screen_long = screen_long
        self.margin = self.screen_long * self.margin_ratio
        self.line_spacing = (self.screen_long - self.margin * 2) / 14
        self.screen = pygame.display.set_mode((self.screen_long, self.screen_long), pygame.RESIZABLE)

        # 加载图标
        icon_path = os.path.join(BASE_DIR, "icon.ico")
        if os.path.exists(icon_path):
            icon = pygame.image.load(icon_path).convert_alpha()
            icon = pygame.transform.scale(icon, (64, 64))
            pygame.display.set_icon(icon)

        self.history = []
        self.click_num = 0

        # 加载音效
        pygame.mixer.init()
        sound_path = os.path.join(BASE_DIR, "click.mp3")
        if os.path.exists(sound_path):
            self.click_sound = pygame.mixer.Sound(sound_path)
        else:
            self.click_sound = None

        self.game_over = False

    def update_params(self, new_screen_long):
        self.screen_long = new_screen_long
        self.margin = self.screen_long * self.margin_ratio
        self.line_spacing = (self.screen_long - self.margin * 2) / 14
        self.screen = pygame.display.set_mode((self.screen_long, self.screen_long), pygame.RESIZABLE)

    def check(self, row, col):
        player = self.matrix[row][col]
        directions = [
            (0, 1), (1, 0), (1, 1), (1, -1)
        ]
        for dr, dc in directions:
            count = 1
            r, c = row + dr, col + dc
            while 0 <= r < 15 and 0 <= c < 15 and self.matrix[r][c] == player:
                count += 1
                r += dr
                c += dc
            r, c = row - dr, col - dc
            while 0 <= r < 15 and 0 <= c < 15 and self.matrix[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            if count >= 5:
                return True
        return False

    def reset_game(self):
        self.matrix = [[0] * 15 for _ in range(15)]
        self.history.clear()
        self.click_num = 0
        self.game_over = False

    def draw(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    new_size = max(300, min(event.w, event.h))
                    self.update_params(new_size)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over:
                        continue
                    x, y = pygame.mouse.get_pos()
                    col = round((x - self.margin) / self.line_spacing)
                    row = round((y - self.margin) / self.line_spacing)
                    if 0 <= row < 15 and 0 <= col < 15:
                        if self.matrix[row][col] == 0:
                            player = 1 if self.click_num % 2 == 0 else 2
                            self.matrix[row][col] = player
                            self.history.append((row, col))
                            self.click_num += 1
                            if self.click_sound:
                                self.click_sound.play()
                            if self.check(row, col):
                                self.game_over = True
                                winner = "黑子" if player == 1 else "白子"
                                messagebox.showinfo("游戏结束", f"玩家 {winner} 获胜！棋盘将自动重置。")
                                self.reset_game()

            self.screen.fill("#F4C47F")

            # 画棋盘线
            for x in range(15):
                start_pos = (self.margin + self.line_spacing * x, self.margin)
                end_pos = (self.margin + self.line_spacing * x, self.screen_long - self.margin)
                pygame.draw.line(self.screen, "#000000", start_pos, end_pos, 2)
            for y in range(15):
                start_pos = (self.margin, self.margin + self.line_spacing * y)
                end_pos = (self.screen_long - self.margin, self.margin + self.line_spacing * y)
                pygame.draw.line(self.screen, "#000000", start_pos, end_pos, 2)

            # 星位
            star_points = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
            for cx, cy in star_points:
                pygame.draw.circle(self.screen, "#000000",
                                   (int(self.margin + self.line_spacing * cx),
                                    int(self.margin + self.line_spacing * cy)),
                                   int(self.line_spacing / 6))

            # 棋子
            for row in range(15):
                for col in range(15):
                    if self.matrix[row][col] != 0:
                        cx = int(col * self.line_spacing + self.margin)
                        cy = int(row * self.line_spacing + self.margin)
                        color = "#000000" if self.matrix[row][col] == 1 else "#FFFFFF"
                        pygame.draw.circle(self.screen, color, (cx, cy), int(self.line_spacing / 2))

            # 鼠标提示方格
            mx, my = pygame.mouse.get_pos()
            grid_x = round((mx - self.margin) / self.line_spacing) * self.line_spacing + self.margin
            grid_y = round((my - self.margin) / self.line_spacing) * self.line_spacing + self.margin
            if 0 <= (grid_x - self.margin) / self.line_spacing < 15 and 0 <= (grid_y - self.margin) / self.line_spacing < 15:
                next_color = "#000000" if self.click_num % 2 == 0 else "#FFFFFF"
                pygame.draw.rect(self.screen, next_color,
                                 [grid_x - self.line_spacing / 2, grid_y - self.line_spacing / 2,
                                  self.line_spacing, self.line_spacing], 3)

            pygame.display.update()


if __name__ == '__main__':
    game_instance = game(900)
    game_instance.draw()
