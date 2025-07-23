from pygame.examples.sprite_texture import renderer

from game_core import GomokuGame
from opengl_renderer import OpenGLRenderer
from ai_player import AIPlayer
import pygame
import opengl_renderer

class AIGame:
    def __init__(self):
        self.game = GomokuGame()
        self.renderer = OpenGLRenderer(self.game)
        self.ai_player = AIPlayer(self.game, self.game.WHITE)  # AI后手（白棋）
        self.human_player = self.game.BLACK  # 人类先手（黑棋）
        self.ai_thinking = True   # True AI黑棋 / False 用户黑棋

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.game.game_over and not self.ai_thinking:
                        if self.renderer.is_click_on_board(event.pos):
                            row, col = self.renderer.screen_to_board(event.pos)
                            if self.game.make_move(int(row), int(col)):
                                # 人类下完后，AI下棋
                                self.ai_thinking = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # 重置游戏
                        self.game.reset_game()
                        self.ai_thinking = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

            # AI回合
            if not self.game.game_over and self.ai_thinking:
                move = self.ai_player.find_best_move()
                if move:
                    row, col = move
                    self.game.make_move(row, col)
                self.ai_thinking = False

            self.renderer.render()
            clock.tick(60)   # 控制帧率，一般不需要修改

        pygame.quit()