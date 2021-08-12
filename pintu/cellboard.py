import pygame
from pygame.locals import *
import random


class CellBoard(object):

    def __init__(self, row, columns, width, height, sound = None):
        self.cells = []
        self.row = row
        self.columns = columns
        self.width = width
        self.height = height
        self.cellNum = self.row * self.columns
        self.i_blank = self.cellNum - 1
        self.restore = False
        self.initialized = False
        self.hint_sound = sound
        self.cell_board_init()

    def cell_board_init(self):

        for i in range(self.cellNum):
            self.cells.append(i)
        self.cells[self.i_blank] = -1
        while True:
            for i in range(50):
                key = K_UP - random.randint(0, 3)
                self.cell_move(key)
            self.restore = self.is_board_be_restore()
            if not self.restore:
                break
        self.initialized = True

    def is_board_be_restore(self):
        for i in range(self.cellNum - 1):
            if not self.cells[i] == i:
                return False
        return True

    def cell_move(self, key):

        if self.initialized and (key == K_LEFT or key == K_RIGHT or key == K_UP or key == K_DOWN):
            self.hint_sound.play()
        if key == K_LEFT:
            if (self.i_blank + 1) % self.columns != 0:
                self.cells[self.i_blank], self.cells[self.i_blank + 1] = \
                    self.cells[self.i_blank + 1], self.cells[self.i_blank]
                self.i_blank = self.i_blank + 1
        elif key == K_RIGHT:
            if self.i_blank % self.columns != 0:
                self.cells[self.i_blank], self.cells[self.i_blank - 1] = \
                    self.cells[self.i_blank - 1], self.cells[self.i_blank]
                self.i_blank = self.i_blank - 1
        elif key == K_UP:
            if self.i_blank // self.columns < (self.row - 1):
                self.cells[self.i_blank], self.cells[self.i_blank + self.columns] = \
                    self.cells[self.i_blank + self.columns], self.cells[self.i_blank]
                self.i_blank += self.columns
        elif key == K_DOWN:
            if self.i_blank // self.columns != 0:
                self.cells[self.i_blank], self.cells[self.i_blank - self.columns] = \
                    self.cells[self.i_blank - self.columns], self.cells[self.i_blank]
                self.i_blank -= self.columns

    def show(self, window):

        black = (0, 0, 0)
        white = (255, 255, 255)
        image_rect = window.bg_image.get_rect()
        #屏幕全白
        window.screen.fill(white)
        #把背景图挨个画上去，除了blank_cell
        for i in range(self.cellNum):
            if self.cells[i] == -1:
                continue
            x, y = i % self.columns, i // self.columns
            rect = pygame.Rect(x * self.width, y * self.height, self.width, self.height)
            area = pygame.Rect((self.cells[i] % self.columns) * self.width, self.cells[i] // self.columns * self.height,
                               self.width, self.height)
            window.screen.blit(window.bg_image, rect, area)
        #画方格
        for i in range(self.columns + 1):
            pygame.draw.line(window.screen, black, (i * self.width, 0), (i * self.width, image_rect.height))
        for i in range(self.row + 1):
            pygame.draw.line(window.screen, black, (0, i * self.height), (image_rect.width, i * self.height))
