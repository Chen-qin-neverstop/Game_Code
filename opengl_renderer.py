import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import tkinter_part

# 渲染模块
'''
用于游戏本体的渲染：
包含棋盘、棋子、按键，以及一些提示文字和落子点是否超出棋盘边界
'''



class OpenGLRenderer:
    def __init__(self, game):
        self.game = game
        self.window_size = (800, 800)
        self.board_size = game.BOARD_SIZE
        self.cell_size = 40
        self.margin = (self.window_size[0] - (self.board_size - 1) * self.cell_size) // 2
        self.piece_radius = 18

        # 初始化Pygame和OpenGL
        pygame.init()
        pygame.display.set_mode(self.window_size, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("五子棋游戏")

        # 设置OpenGL视口
        glViewport(0, 0, self.window_size[0], self.window_size[1])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # gluOrtho2D(0, self.window_size[0], self.window_size[1], 0)   // 棋子落点y轴反了
        gluOrtho2D(0, self.window_size[0], 0, self.window_size[1])
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # 启用2D纹理和混合
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # 颜色定义
        self.colors = {
            'background': (0.85, 0.72, 0.55, 1.0),
            'grid': (0.0, 0.0, 0.0, 1.0),
            'black': (0.0, 0.0, 0.0, 1.0),
            'white': (1.0, 1.0, 1.0, 1.0),
            'highlight': (1.0, 0.0, 0.0, 1.0),
            'text': (0.2, 0.2, 0.2, 1.0),
            'text1':(0.1, 0.1, 0.2, 0.3)
        }

    def draw_board(self):
        # 绘制背景
        glColor4f(*self.colors['background'])
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.window_size[0], 0)
        glVertex2f(self.window_size[0], self.window_size[1])
        glVertex2f(0, self.window_size[1])
        glEnd()

        # 绘制网格线
        glColor4f(*self.colors['grid'])
        glLineWidth(1.5)

        # 横线
        for i in range(self.board_size):
            y = self.margin + i * self.cell_size
            glBegin(GL_LINES)
            glVertex2f(self.margin, y)
            glVertex2f(self.margin + (self.board_size - 1) * self.cell_size, y)
            glEnd()

        # 竖线
        for i in range(self.board_size):
            x = self.margin + i * self.cell_size
            glBegin(GL_LINES)
            glVertex2f(x, self.margin)
            glVertex2f(x, self.margin + (self.board_size - 1) * self.cell_size)
            glEnd()

        # 绘制棋盘上的五个点
        glColor4f(*self.colors['grid'])
        for point in [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]:
            x = self.margin + point[0] * self.cell_size
            y = self.margin + point[1] * self.cell_size
            self.draw_circle(x, y, 4)

    def draw_pieces(self):
        board = self.game.get_board()
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] != self.game.EMPTY:
                    x = self.margin + col * self.cell_size
                    y = self.margin + row * self.cell_size

                    if board[row][col] == self.game.BLACK:
                        glColor4f(*self.colors['black'])
                    else:
                        glColor4f(*self.colors['white'])

                    self.draw_circle(x, y, self.piece_radius)

                # 有问题（禁用）
                    # # 为白棋添加黑色边框
                    # if board[row][col] == self.game.WHITE:
                    #     glColor4f(0, 0, 0, 1)
                    #     glLineWidth(1.0)
                    #     self.draw_circle(x, y, self.piece_radius, filled=False)

        # 绘制最后一步落子的标记
        if self.game.move_history:
            last_row, last_col = self.game.move_history[-1]
            x = self.margin + last_col * self.cell_size
            y = self.margin + last_row * self.cell_size

            glColor4f(*self.colors['highlight'])
            self.draw_circle(x, y, 5)

    def draw_circle(self, x, y, radius, filled=True):
        segments = 32
        glBegin(GL_TRIANGLE_FAN if filled else GL_LINE_LOOP)
        glVertex2f(x, y)
        for i in range(segments + 1):
            angle = 2 * np.pi * i / segments
            glVertex2f(x + radius * np.cos(angle), y + radius * np.sin(angle))
        glEnd()

    def draw_ui(self):
        # 显示当前玩家信息
        player_text = f"当前玩家: {'黑棋' if self.game.current_player == self.game.BLACK else '白棋'}"
        player_state = f"状态: {'先手回合' if self.game.current_player == self.game.BLACK else '后手回合'}"
        self.render_text(player_text, 600,750 , self.colors['text'])
        self.render_text(player_state, 600, 700, self.colors['text1'])

        # 显示游戏状态
        if self.game.game_over:
            if self.game.winner:
                winner_text = f"{'黑棋' if self.game.winner == self.game.BLACK else '白棋'}获胜!"
            else:
                winner_text = "平局!"
            self.render_text(winner_text, self.window_size[0] // 2, 30,
                             (1, 0, 0, 1) if self.game.winner else (0.5, 0.5, 0.5, 1))
            # tkinter_part.win(self)
            tkinter_part.create_windows('tkinter_renderer\\认可.jpg')

    def render_text(self, text, x, y, color):
        # 使用Pygame渲染文字到纹理
        font = pygame.font.SysFont('SimHei', 24)
        text_surface = font.render(text, True, (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255)))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)

        # 创建纹理
        glEnable(GL_TEXTURE_2D)
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_surface.get_width(), text_surface.get_height(),
                     0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)

        # 绘制纹理四边形
        glColor4f(1, 1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0);
        glVertex2f(x, y)
        glTexCoord2f(1, 0);
        glVertex2f(x + text_surface.get_width(), y)
        glTexCoord2f(1, 1);
        glVertex2f(x + text_surface.get_width(), y + text_surface.get_height())
        glTexCoord2f(0, 1);
        glVertex2f(x, y + text_surface.get_height())
        glEnd()

        # 清理纹理
        glDeleteTextures(1, [texture])

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.draw_board()
        self.draw_pieces()
        self.draw_ui()

        pygame.display.flip()

    def screen_to_board(self, pos):
        x, y = pos
        # 关键：翻转 Y 轴，让 Pygame 鼠标坐标适配 OpenGL 正交投影
        y = self.window_size[1] - y
        col = round((x - self.margin) / self.cell_size)
        row = round((y - self.margin) / self.cell_size)
        return row, col
    # 是否超出棋盘边界
    def is_click_on_board(self, pos):
        row, col = self.screen_to_board(pos)
        return (0 <= row < self.board_size and
                0 <= col < self.board_size)