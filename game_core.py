import numpy as np
from audio_manager import AudioManager

'''
五子棋游戏的输赢判定逻辑：
1.五子连珠（四个方向）
2.check_win_for_position<————是否已经获胜<————check_win
3.落子是否合法
4.棋盘状态检查————深拷贝Numpy数组（为了不影响原来对象）
'''

class GomokuGame:
    def get_neighbors(self, row, col, radius=1):
        """获取指定位置的相邻非空棋子数量"""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                    if self.board[r][c] != self.EMPTY:
                        count += 1
        return count
    BOARD_SIZE = 15
    EMPTY = 0
    BLACK = 1
    WHITE = 2
#  棋盘状态判定

    def __init__(self):
        # 用Numpy数组来存储棋盘
        self.board = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE), dtype=int)
        self.current_player = self.BLACK
        self.game_over = False
        self.winner = None
        self.move_history = []   # 记录棋盘的状态（历史记录） 记录（row,col）
        
        # 初始化音频管理器
        self.audio = AudioManager()
        
    def initialize_audio(self, piece_sound_path=None, win_sound_path=None, bgm_path=None):
        """初始化游戏音频"""
        if piece_sound_path:
            self.audio.load_sound('piece', piece_sound_path)
        if win_sound_path:
            self.audio.load_sound('win', win_sound_path)
        if bgm_path:
            self.audio.load_background_music(bgm_path)
            self.audio.play_background_music()

    def reset_game(self):   # 重置
        self.board.fill(self.EMPTY)
        self.current_player = self.BLACK
        self.game_over = False
        self.winner = None
        self.move_history = []
        # 重新开始背景音乐
        self.audio.play_background_music()

    def make_move(self, row, col):
        # 落子位置检查
        if self.game_over or not self.is_valid_move(row, col):
            return False

        self.board[row][col] = self.current_player
        self.move_history.append((row, col))
        
        # 播放落子音效
        self.audio.play_sound('piece')

        if self.check_win(row, col):     # 判定是否游戏结束
            self.game_over = True
            self.winner = self.current_player
            # 播放胜利音效
            self.audio.play_sound('win')
        elif self.is_board_full():
            self.game_over = True
        else:
            self.switch_player()

        return True

    def is_valid_move(self, row, col):    # 验证落子可行性
        return (0 <= row < self.BOARD_SIZE and
                0 <= col < self.BOARD_SIZE and
                self.board[row][col] == self.EMPTY)

    def switch_player(self):   # 选手转换
        self.current_player = self.WHITE if self.current_player == self.BLACK else self.BLACK

    def check_win(self, row, col):    # 如果下当前棋子是否会胜利
        player = self.board[row][col]
        directions = [   # 这里表示的是变化量
            [(0, 1), (0, -1)],  # 水平 dx=0，列变化
            [(1, 0), (-1, 0)],  # 垂直 dy=0，列变化
            [(1, 1), (-1, -1)],  # 对角线
            [(1, -1), (-1, 1)]  # 反对角线
        ]

        for direction_pair in directions:
            count = 1  # 当前位置的棋子

            # 检查两个相反方向
            for dx, dy in direction_pair:
                r, c = row + dx, col + dy
                while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                    if self.board[r][c] == player:
                        count += 1
                        if count >= 5:
                            return True
                    else:
                        break
                    r += dx
                    c += dy

        return False

    def check_win_for_position(self, player):
        """检查指定玩家是否已经获胜"""
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == player:
                    if self.check_win(row, col):
                        return True
        return False

    def is_board_full(self):
        return np.all(self.board != self.EMPTY)

    def get_board(self):
        return self.board.copy()