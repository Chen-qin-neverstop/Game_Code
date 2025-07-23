from game_core import GomokuGame
from opengl_renderer import OpenGLRenderer
import pygame
from OpenGL.GL import *

# 本地双人对弈
class LocalGame:
    def __init__(self):
        self.game = GomokuGame()
        self.renderer = OpenGLRenderer(self.game)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.game.game_over and self.renderer.is_click_on_board(event.pos):
                        row, col = self.renderer.screen_to_board(event.pos)
                        self.game.make_move(int(row), int(col))
            # check_win包含在make_move的实现中，每次落子都会判定
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 重置游戏
                        self.game.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            self.renderer.render()
            clock.tick(60)

        pygame.quit()