import numpy as np
from collections import defaultdict, deque
from typing import List, Tuple, Set, Optional

class AIPlayer:
    """
    五子棋AI玩家类，基于Minimax算法和Alpha-Beta剪枝优化
    目前防守可以，但是攻击性不够, 当AI为黑棋时，会存在白棋四子但是黑棋不防的情况。
    应该是评分函数有问题，需要对进攻模式进行优化（本质是算法的问题），需要对白棋和黑棋的情况分开判断
    """

    def __init__(self, game, player, debug_mode=True):
        self.debug_mode = debug_mode
        """
        初始化AI玩家
        :param game: GomokuGame实例
        :param player: 该AI控制的棋子颜色（BLACK/WHITE）
        """
        self.game = game
        self.player = player
        self.opponent = game.BLACK if player == game.WHITE else game.WHITE

        # 算法参数配置
        self.max_depth = 3  # 最大搜索深度
        self.expand_radius = 1  # 落子扩展半径
        self.pattern_scores = {
            # 进攻模式评分（黑棋视角）  针对这种情况进行修改
            "B0000": 1, "0B000": 1, "00B00": 1, "000B0": 1, "0000B": 1,
            "BB000": 10, "0BB00": 10, "00BB0": 10, "000BB": 10,
            "B0B00": 10, "0B0B0": 10, "00B0B": 10, "B00B0": 10, "0B00B": 10, "B000B": 10,
            "BBB00": 100, "0BBB0": 100, "00BBB": 100, "BB0B0": 100, "0BB0B": 100,
            "B0BB0": 100, "0B0BB": 100, "BB00B": 100, "B00BB": 100, "B0B0B": 100,
            "BBBB0": 10000, "BBB0B": 10000, "BB0BB": 10000, "B0BBB": 10000, "0BBBB": 10000,
            "BBBBB": 1000000,
            # 防守模式评分（白棋视角）
            "W0000": 1, "0W000": 1, "00W00": 1, "000W0": 1, "0000W": 1,
            "WW000": 10, "0WW00": 10, "00WW0": 10, "000WW": 10,
            "W0W00": 10, "0W0W0": 10, "00W0W": 10, "W00W0": 10, "0W00W": 10, "W000W": 10,
            "WWW00": 1000, "0WWW0": 2000, "00WWW": 1000, "WW0W0": 1000, "0WW0W": 1000,
            "W0WW0": 1000, "0W0WW": 1000, "WW00W": 1000, "W00WW": 1000, "W0W0W": 1000,
            "WWWW0": 100000, "WWW0W": 100000, "WW0WW": 100000, "W0WWW": 100000, "0WWWW": 100000,
            "WWWWW": 10000000
        }

    def get_possible_moves(self) -> List[Tuple[int, int]]:
        """
        获取可能的落子位置（基于扩展半径）
        :return: 可落子的(x,y)坐标列表
        """
        board = self.game.board
        moves = set()

        # 查找已有棋子周围的空位
        for i in range(15):
            for j in range(15):
                if board[i][j] != self.game.EMPTY:
                    for dx in range(-self.expand_radius, self.expand_radius + 1):
                        for dy in range(-self.expand_radius, self.expand_radius + 1):
                            x, y = i + dx, j + dy
                            if 0 <= x < 15 and 0 <= y < 15 and board[x][y] == self.game.EMPTY:
                                moves.add((x, y))

        # 开局时返回中心点
        if not moves:
            return [(7, 7)]
        return list(moves)

    def evaluate_position(self) -> int:
        """
        评估当前棋盘局面
        :return: 局面评分（正数对AI有利）
        """
        score = 0
        board = self.game.board

        # 转换棋盘状态为字符表示
        def to_char(cell):
            if cell == self.game.BLACK: return 'B'
            if cell == self.game.WHITE: return 'W'
            return '0'

        # 检查所有可能的五元组
        for i in range(15):
            for j in range(15):
                # 水平方向
                if j + 4 < 15:
                    pattern = ''.join([to_char(board[i][j + k]) for k in range(5)])
                    score += self.pattern_scores.get(pattern, 0)

                # 垂直方向
                if i + 4 < 15:
                    pattern = ''.join([to_char(board[i + k][j]) for k in range(5)])
                    score += self.pattern_scores.get(pattern, 0)

                # 对角线方向
                if i + 4 < 15 and j + 4 < 15:
                    pattern = ''.join([to_char(board[i + k][j + k]) for k in range(5)])
                    score += self.pattern_scores.get(pattern, 0)

                # 反对角线方向
                if i + 4 < 15 and j - 4 >= 0:
                    pattern = ''.join([to_char(board[i + k][j - k]) for k in range(5)])
                    score += self.pattern_scores.get(pattern, 0)

        # 如果是白棋AI，需要反转评分
        if self.player == self.game.WHITE:
            score = -score

        return score

    def minimax(self, depth: int, alpha: int, beta: int, is_maximizing: bool) -> int:
        """
        Minimax算法核心，带Alpha-Beta剪枝
        :param depth: 当前搜索深度
        :param alpha: Alpha值
        :param beta: Beta值
        :param is_maximizing: 是否最大化层
        :return: 最佳评估值
        """
        # 终止条件检查
        winner = self.check_winner()
        if winner == self.player:
            return 1000000 - depth  # 优先短路径胜利
        elif winner == self.opponent:
            return -1000000 + depth
        elif depth == 0 or self.game.is_board_full():
            return self.evaluate_position()

        # 生成候选走法
        moves = self.get_possible_moves()
        if not moves:
            return 0

        if is_maximizing:
            max_score = -float('inf')
            for move in moves:
                # 模拟落子
                self.game.board[move[0]][move[1]] = self.player
                score = self.minimax(depth - 1, alpha, beta, False)
                # 撤销落子
                self.game.board[move[0]][move[1]] = self.game.EMPTY

                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  # Alpha-Beta剪枝
            return max_score
        else:
            min_score = float('inf')
            for move in moves:
                # 模拟对手落子
                self.game.board[move[0]][move[1]] = self.opponent
                score = self.minimax(depth - 1, alpha, beta, True)
                # 撤销落子
                self.game.board[move[0]][move[1]] = self.game.EMPTY

                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break  # Alpha-Beta剪枝
            return min_score

    # 只传self的胜利判定————跟game_core()中check_win区别
    # 检查当前棋盘是否有五子连珠————两个或许可以

    def check_winner(self) -> Optional[int]:
        """
        检查当前棋盘是否有获胜方
        :return: 获胜方（BLACK/WHITE）或None
        """
        board = self.game.board
        # 检查所有可能的五连珠
        for i in range(15):
            for j in range(15):
                if board[i][j] == self.game.EMPTY:
                    continue

                # 水平方向
                if j + 4 < 15 and all(board[i][j + k] == board[i][j] for k in range(5)):
                    return board[i][j]

                # 垂直方向
                if i + 4 < 15 and all(board[i + k][j] == board[i][j] for k in range(5)):
                    return board[i][j]

                # 对角线方向
                if i + 4 < 15 and j + 4 < 15 and all(board[i + k][j + k] == board[i][j] for k in range(5)):
                    return board[i][j]

                # 反对角线方向
                if i + 4 < 15 and j - 4 >= 0 and all(board[i + k][j - k] == board[i][j] for k in range(5)):
                    return board[i][j]
        return None

    def find_best_move(self) -> Tuple[int, int]: # 元组类型，顺序+数量+类型固定
        """
        寻找最佳落子位置
        :return: (x, y) 最佳落子坐标
        """
        best_score = -float('inf')
        best_move = None
        alpha = -float('inf')
        beta = float('inf')

        # 获取所有可能走法
        moves = self.get_possible_moves()
        if not moves:
            return (7, 7)  # 默认中心点

        # 遍历所有可能的走法
        for move in moves:
            # 模拟落子
            self.game.board[move[0]][move[1]] = self.player
            # 评估局面
            score = self.minimax(self.max_depth - 1, alpha, beta, False)
            # 撤销落子
            self.game.board[move[0]][move[1]] = self.game.EMPTY

            # 更新最佳走法
            if self.debug_mode:
                print(f"候选坐标 ({move[0]},{move[1]}) 评分 {score:.1f}")

            if score > best_score:
                best_score = score
                best_move = move
                if self.debug_mode:
                    print(f"↑ 新最佳坐标 ({best_move[0]},{best_move[1]})")
            alpha = max(alpha, best_score)

        if self.debug_mode:
            print(f"[AI决策] 最终选择坐标 ({best_move[0]},{best_move[1]}) 评分 {best_score} (搜索深度 {self.max_depth})")
        return best_move if best_move else moves[0]



