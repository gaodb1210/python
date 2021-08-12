# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import time

import pygame

import chessBoard
from chessBoard import ChessBoard

# Press the green button in the gutter to run the script.


def run_game():

    board = ChessBoard()
    board.draw()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over and event.type == pygame.KEYDOWN:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and (not game_over):
                if event.button == 1:  # 按下的是鼠标左键
                    board.drop_it(event.pos)
                    if board.is_win():
                        if board.black_turn:
                            text = '黑方获胜，按任意键继续'
                        else:
                            text = '白方获胜，按任意键继续'
                        game_over_text = font.render(text, True, (255, 0, 0))
                        board.chessboard().blit(game_over_text, (round(width / 2 - game_over_text.get_width() / 2),
                                                                 round(height / 2 - game_over_text.get_height() / 2)))
                        game_over = True

            screen.blit(board.chessboard(), (0, 0))
            pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    size = width, height = 824, 824
    screen = pygame.display.set_mode(size, 0, 32)
    pygame.display.set_caption('五子棋')
    font = pygame.font.Font('./font/font.ttf', 48)
    clock = pygame.time.Clock()  # 设置时钟
    while True:
        clock.tick(20)  # 设置帧率
        run_game()

