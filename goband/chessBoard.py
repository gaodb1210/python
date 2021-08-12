from collections import namedtuple

import pygame

EMPTY = 0
WHITE_CHESS = 1
BLACK_CHESS = 2

Point = namedtuple('Point', ['x', 'y'])


class Position:
    def __init__(self, x, y, chess):
        self.point = Point(x, y)
        self.chess = chess


class ChessBoard:

    def __init__(self):

        self.back_ground_file = "./image/bg.jpg"
        self.white_chess_file = "./image/white_chess.png"
        self.black_chess_file = "./image/black_chess.png"
        self.color = (0, 0, 0)
        self.chess_board = pygame.image.load(self.back_ground_file)
        self.white_chess = pygame.image.load(self.white_chess_file).convert_alpha()
        self.black_chess = pygame.image.load(self.black_chess_file).convert_alpha()
        self.chess_rect = self.black_chess.get_rect()
        self.black_turn = True
        self.win = False
        self.points = [[] for i in range(15)]
        self.white_chess_count = 0
        self.black_chess_count = 0
        self.n = 0

        self.top, self.left, self.space, self.lines = (20, 20, 56, 15)
        for i in range(self.lines):
            for j in range(self.lines):
                self.points[i].append(Position(self.top + j * self.space, self.left + i * self.space, EMPTY))

    def drop_it(self, pos):
        col, row = self.get_board_point(pos)
        draw_pos_x = self.points[row][col].point.x - int(self.chess_rect.width / 2)
        draw_pos_y = self.points[row][col].point.y - int(self.chess_rect.height / 2)
        point = self.points[row][col]
        if point.chess != EMPTY:
            return
        if self.black_turn:
            self.chess_board.blit(self.black_chess, (draw_pos_x, draw_pos_y))
            self.points[row][col].chess = BLACK_CHESS
            self.black_chess_count += 1
        else:
            self.chess_board.blit(self.white_chess, (draw_pos_x, draw_pos_y))
            self.points[row][col].chess = WHITE_CHESS
            self.white_chess_count += 1

        self.win = self.check_win(row, col)

        if not self.win:
            # 交换棋子颜色
            self.black_turn = not self.black_turn

    def draw(self):
        for x in range(self.lines):
            pygame.draw.line(self.chess_board, self.color, self.points[0][x].point, self.points[self.lines - 1][x].point)
            pygame.draw.line(self.chess_board, self.color, self.points[x][0].point, self.points[x][self.lines - 1].point)

    def get_board_point(self, pos):
        x, y = pos
        i, j = (0, 0)
        oppo_x = x - self.left
        if oppo_x > 0:
            i = round(oppo_x / self.space)  # 四舍五入取整
        oppo_y = y - self.top
        if oppo_y > 0:
            j = round(oppo_y / self.space)
        return i, j

    def check_win(self, row, col):

        chess = self.points[row][col].chess
        if self.get_chess_count(chess) < 5:
            return False

        # 检查水平方向
        count = 1
        if row != 0:
            for i in range(row - 1, 0, -1):
                if self.points[i][col].chess != chess:
                    break
                else:
                    count += 1
        if row != self.lines - 1:
            for i in range(row + 1, self.lines - 1):
                if self.points[i][col].chess != chess:
                    break
                count += 1
        if count >= 5:
            return True

        # 检查垂直方向
        count = 1
        if col > 0:
            for i in range(1, col):
                c_col = col - i
                c_point = self.points[row][c_col]
                if c_point.chess != chess:
                    break
                count += 1
        if col < self.lines - 1:
            for i in range(col + 1, self.lines):
                c_col = i
                c_point = self.points[row][c_col]
                if c_point.chess != chess:
                    break
                count += 1
        if count >= 5:
            return True

        # 检查斜方向
        count = 1
        for n in range(1, self.lines - max(row, col)):
            c_row = row - n
            c_col = col + n
            if c_row < 0 or c_col < 0:
                break
            c_point = self.points[c_row][c_col]
            if c_point.chess != chess:
                break
            count += 1
        for n in range(1, min(self.lines - row - 1, col)):
            c_row = row + n
            c_col = col - n
            if c_row < 0 or c_col < 0:
                break
            c_point = self.points[c_row][c_col]
            if c_point.chess != chess:
                break
            count += 1
        if count >= 5:
            return True

        # 检查反斜方向
        count = 1
        for n in range(1, min(row, col)):
            c_row = row - n
            c_col = col - n
            if c_row < 0 or c_col < 0:
                break
            c_point = self.points[c_row][c_col]
            if c_point.chess != chess:
                break
            count += 1
        for n in range(1, self.lines - max(row, col)):
            c_row = row + n
            c_col = col + n
            if c_row < 0 or c_col < 0:
                break
            c_point = self.points[c_row][c_col]
            if c_point.chess != chess:
                break
            count += 1
        if count >= 5:
            return True

        return False

    def chessboard(self):
        return self.chess_board

    def is_win(self):
        return self.win

    def get_chess_count(self, chess):
        if chess == WHITE_CHESS:
            return self.white_chess_count
        else:
            return self.black_chess_count

    def reset(self):
        for i in range(self.lines):
            for j in range(self.lines):
                point = self.points[i][j]
                if point.chess != EMPTY:
                    self.chess_board.blit()
                    self.points[i][j].chess = EMPTY
