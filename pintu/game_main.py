# encoding: utf-8
import os, sys
import random, pygame
from pygame.locals import *
from cellboard import CellBoard
from config import *

White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)


class Window(object):

    def __init__(self, screen, bg_image):

        self.bg_image = pygame.image.load(bg_image)
        rect = self.bg_image.get_rect()
        self.size = (rect.width, rect.height)
        self.screen = screen
        self.game_board = None
        self.hint_sound = None

    def game_board_create(self, level):

        ImageRect = self.bg_image.get_rect()
        cell_width = ImageRect.width // level
        cell_height = ImageRect.height // level
        self.game_board = CellBoard(level, level, cell_width, cell_height, self.hint_sound)

    def hint_sound_load(self, sound, volume):
        self.hint_sound = pygame.mixer.Sound(sound)
        self.hint_sound.set_volume(volume)

    # game start and end interface
    def show_start_interface(self):

        width, height = self.size
        image = pygame.image.load('./image/bg2.jpg')
        t_font = pygame.font.Font(FONT_FILE, width // 10)
        c_font = pygame.font.Font(FONT_FILE, width // 20)
        l_font = pygame.font.Font(FONT_FILE, width // 20)
        l_font.set_underline(1)
        l_font.set_italic(1)
        title = t_font.render('拼图游戏', True, Red)
        tips = c_font.render('-请选择游戏级别', True, Blue)
        level_1 = l_font.render('*level 1', True, Green)
        level_2 = l_font.render('*level 2', True, Green)
        level_3 = l_font.render('*level 3', True, Green)
        t_rect = title.get_rect()
        t_rect.midtop = (width / 2.5, height / 10)
        tips_rect = tips.get_rect()
        tips_rect.midtop = (width / 2.2, height / 4)
        start_h = height / 3.2
        level_1_rect = level_1.get_rect()
        level_1_rect.midtop = (width / 2, start_h)
        start_h += level_1_rect.height
        level_2_rect = level_1.get_rect()
        level_2_rect.midtop = (width / 2, start_h)
        start_h += level_2_rect.height
        level_3_rect = level_1.get_rect()
        level_3_rect.midtop = (width / 2, start_h)
        self.screen.blit(image, (0, 0))
        self.screen.blit(title, t_rect)
        self.screen.blit(tips, tips_rect)
        self.screen.blit(level_1, level_1_rect)
        self.screen.blit(level_2, level_2_rect)
        self.screen.blit(level_3, level_3_rect)
        pygame.display.update()
        size = 0
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    stop_game()
                if event.type == MOUSEBUTTONDOWN:
                    if self.is_pos_in_rect(event.pos, level_1_rect):
                        size = 3
                    elif self.is_pos_in_rect(event.pos, level_2_rect):
                        size = 4
                    elif self.is_pos_in_rect(event.pos, level_3_rect):
                        size = 5
            if size:
                break
        return size

    def show_end_interface(self):

        width, height = self.size
        t_font = pygame.font.Font(FONT_FILE, width // 15)
        t_font.set_italic(1)
        e_font = pygame.font.Font(FONT_FILE, width // 20)
        e_font.set_italic(1)
        e_font.set_underline(1)
        tip = t_font.render('success', True, Blue)
        tip_rect = tip.get_rect()
        tip_rect.midtop = width / 4, height / 8
        c_title = e_font.render('*continue*', True, Blue)
        c_rect = c_title.get_rect()
        c_rect.midtop = width / 2, height / 2
        e_title = e_font.render('*exit*', True, Blue)
        e_rect = e_title.get_rect()
        e_rect.midtop = width / 2, height / 3
        self.screen.fill(White)
        pygame.display.update()
        pygame.time.wait(100)
        self.screen.blit(self.bg_image, (0, 0))
        self.screen.blit(tip, tip_rect)
        self.screen.blit(c_title, c_rect)
        self.screen.blit(e_title, e_rect)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    stop_game()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        stop_game()
                if event.type == MOUSEBUTTONDOWN:
                    if self.is_pos_in_rect(event.pos, c_rect):
                        return True
                    elif self.is_pos_in_rect(event.pos, e_rect):
                        stop_game()

    @staticmethod
    def is_pos_in_rect(pos, rect):
        left, top = pos
        if rect.left <= left <= (rect.left + rect.width) and rect.top <= top <= (rect.top + rect.height):
            return True
        return False


def stop_game():
    pygame.quit()
    sys.exit()


def event_loop(board):
    cell_h = board.height
    cell_w = board.width
    for event in pygame.event.get():
        if event.type == QUIT:
            stop_game()
        if event.type == KEYDOWN:
            board.cell_move(event.key)
        if event.type == MOUSEBUTTONDOWN:
            left, top = event.pos
            index = (left // cell_w) + (top // cell_h) * board.columns
            if index == board.i_blank + 1:
                board.cell_move(K_LEFT)
            elif index == board.i_blank - 1:
                board.cell_move(K_RIGHT)
            elif index == board.i_blank + board.columns:
                board.cell_move(K_UP)
            elif index == board.i_blank - board.columns:
                board.cell_move(K_DOWN)


def board_image_get(path):
    files = [f for f in os.listdir(path) if f.endswith('.jpg') and not f == 'bg2.jpg']
    if files:
        rand_num = random.randint(0, len(files) - 1)
        return os.path.join(path, files[rand_num])
    return None


def bg_music_load(bg_music, volume=0.2):
    pygame.mixer.music.load(bg_music)
    pygame.mixer.music.set_volume(volume)


def bg_music_play():
    pygame.mixer.music.play(-1)


def bg_music_pause():
    pygame.mixer.music.pause()


def bg_music_stop():
    pygame.mixer.music.stop()


def game_board_run(screen):
    image_file = board_image_get(IMAGE_PATH)
    if not image_file:
        print('can not load bg image')
        return -1
    window = Window(screen, image_file)
    window.hint_sound_load(HINT_SOUND_FILE, HINT_SOUND_VOLUME)
    level = window.show_start_interface()
    window.game_board_create(level)
    while True:
        # 事件轮训
        event_loop(window.game_board)
        # 判断游戏是否结束
        if window.game_board.is_board_be_restore():
            return window.show_end_interface()
        window.game_board.show(window)
        pygame.display.update()


def main():
    pygame.init()
    pygame.mixer.init()
    main_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((700, 700))
    pygame.display.set_caption('拼图游戏')
    # 加载音乐
    bg_music_load(BG_MUSIC_FILE, BG_MUSIC_VOLUME)
    bg_music_play()
    while True:
        game_board_run(screen)
        main_clock.tick(40)


if __name__ == '__main__':
    sys.exit(main())
