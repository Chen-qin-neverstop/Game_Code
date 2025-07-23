import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from local_game import LocalGame
from network_game import NetworkGame
from ai_game import AIGame

'''
Function:
1.主菜单的绘制
2.不同模式跳转的接口
3.网络模式子菜单
'''

class MainMenu:
    def __init__(self):
        self.window_size = (800, 600)
        pygame.init()
        pygame.display.set_mode(self.window_size, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("五子棋游戏 - 主菜单")

        glViewport(0, 0, self.window_size[0], self.window_size[1])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.window_size[0], self.window_size[1], 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.buttons = [
            {"text": "本地双人对战", "rect": pygame.Rect(300, 200, 200, 50), "action": self.start_local_game},
            {"text": "联网对战", "rect": pygame.Rect(300, 280, 200, 50), "action": self.start_network_menu},
            {"text": "人机对战", "rect": pygame.Rect(300, 360, 200, 50), "action": self.start_ai_game},
            {"text": "退出游戏", "rect": pygame.Rect(300, 440, 200, 50), "action": self.quit_game}
        ]

        self.network_buttons = [
            {"text": "创建房间", "rect": pygame.Rect(300, 200, 200, 50),
             "action": lambda: self.start_network_game(True)},
            {"text": "加入房间", "rect": pygame.Rect(300, 280, 200, 50),
             "action": lambda: self.start_network_game(False)},
            {"text": "返回", "rect": pygame.Rect(300, 360, 200, 50), "action": self.show_main_menu}
        ]

        self.current_menu = "main"

    def render_text(self, text, x, y, color=(0, 0, 0, 1), size=24):
        """修复文本渲染的核心方法"""
        try:
            # 字体回退机制
            font = pygame.font.SysFont(['SimHei', 'Arial', 'sans-serif'], size)
        except:   #  if try failed use default
            font = pygame.font.SysFont(None, size)

        # 创建带Alpha通道的Surface
        text_surface = pygame.Surface((font.size(text)[0] + 10, font.size(text)[1] + 10), pygame.SRCALPHA)

        # 渲染文本到Surface（颜色值0-255范围）
        text_surface.blit(
            font.render(text, True, (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))),
            (5, 5)
        )

        # 转换为OpenGL纹理数据（关键修复）
        text_data = pygame.image.tostring(text_surface, "RGBA", False)  # 注意这里用False

        # OpenGL纹理设置
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA,
            text_surface.get_width(), text_surface.get_height(),
            0, GL_RGBA, GL_UNSIGNED_BYTE, text_data
        )

        # 绘制纹理
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

        glDeleteTextures([texture])

    def draw_button(self, button):
        """绘制按钮（修复版）"""
        # 1. 绘制按钮背景
        glColor4f(0.7, 0.7, 0.9, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(button["rect"].left, button["rect"].top)
        glVertex2f(button["rect"].right, button["rect"].top)
        glVertex2f(button["rect"].right, button["rect"].bottom)
        glVertex2f(button["rect"].left, button["rect"].bottom)
        glEnd()

        # 2. 绘制按钮边框
        glColor4f(0.3, 0.3, 0.5, 1.0)
        glLineWidth(2.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(button["rect"].left, button["rect"].top)
        glVertex2f(button["rect"].right, button["rect"].top)
        glVertex2f(button["rect"].right, button["rect"].bottom)
        glVertex2f(button["rect"].left, button["rect"].bottom)
        glEnd()

        # 3. 绘制按钮文字（关键修复部分）
        # 先获取文本实际尺寸
        font = pygame.font.SysFont('SimHei', 24)
        text_surface = font.render(button["text"], True, (0, 0, 0))

        # 计算居中位置
        text_x = button["rect"].centerx - text_surface.get_width() // 2
        text_y = button["rect"].centery - text_surface.get_height() // 2

        # 渲染文字（使用黑色确保可见性）
        self.render_text(button["text"], text_x, text_y, (0, 0, 0, 1), 24)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glEnable(GL_BLEND)

        # 绘制背景
        glColor4f(0.9, 0.85, 0.8, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.window_size[0], 0)
        glVertex2f(self.window_size[0], self.window_size[1])
        glVertex2f(0, self.window_size[1])
        glEnd()

        # 绘制标题
        self.render_text("五子棋游戏", self.window_size[0] // 2 - 100, 80, (0.2, 0.2, 0.4, 1), 48)

        # 绘制按钮
        buttons = self.buttons if self.current_menu == "main" else self.network_buttons
        for button in buttons:
            self.draw_button(button)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()  # 获取鼠标位置
                buttons = self.buttons if self.current_menu == "main" else self.network_buttons
                for button in buttons:
                    # 检查鼠标点击位置是否在按钮范围内
                    if button["rect"].collidepoint(pos):   # pygame中的矩形碰撞函数
                        button["action"]()   # 执行对应的操作

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if self.current_menu == "network":
                    self.show_main_menu()
                else:
                    return False

        return True

    def start_local_game(self):
        local_game = LocalGame()
        # 初始化音频
        local_game.game.initialize_audio(
            piece_sound_path='audio_resources/piece.mp3',
            win_sound_path='audio_resources/win.mp3',
            bgm_path='audio_resources/background.mp3'
        )
        local_game.run()
        pygame.display.set_mode(self.window_size, DOUBLEBUF | OPENGL)

    # 定义联机模式子菜单
    def start_network_menu(self):
        self.current_menu = "network"

    def show_main_menu(self):
        self.current_menu = "main"

    def start_network_game(self, is_server):
        network_game = NetworkGame(is_server=is_server)
        # 初始化音频
        network_game.game.initialize_audio(
            piece_sound_path='audio_resources/piece.mp3',
            win_sound_path='audio_resources/win.mp3',
            bgm_path='audio_resources/background.mp3'
        )
        network_game.run()
        pygame.display.set_mode(self.window_size, DOUBLEBUF | OPENGL)

    def start_ai_game(self):
        ai_game = AIGame()
        # 初始化音频
        ai_game.game.initialize_audio(
            piece_sound_path='audio_resources/piece.mp3',
            win_sound_path='audio_resources/win.mp3',
            bgm_path='audio_resources/background.mp3'
        )
        ai_game.run()
        pygame.display.set_mode(self.window_size, DOUBLEBUF | OPENGL)

    def quit_game(self):
        pygame.quit()
        return False

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            running = self.handle_events()
            self.render()
            clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    menu = MainMenu()
    menu.run()