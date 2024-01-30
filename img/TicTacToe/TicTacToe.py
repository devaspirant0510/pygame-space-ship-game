import pygame, sys, random
from pygame.locals import *
from tttAI import *

width = 300
height = 400

center_x = width // 2
center_y = (height - 30) // 2
box_size = 80
text_size = 50

top = center_y - box_size - box_size // 2
down = top + box_size * 3
left = center_x - box_size - box_size // 2
right = left + box_size * 3

fps = 30
fps_clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)

def main():
    pygame.init()
    surface = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Tic Tac Toe')
    surface.fill(white)
    menu = Menu(surface)
    ttt = TTT(surface, menu)
    while True:
        run_game(surface, menu, ttt)
        menu.is_continue()

def run_game(surface, menu, ttt):
    reset_game(surface, menu, ttt)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == MOUSEBUTTONUP:
                if ttt.check_board(event.pos):
                    if ttt.check_gameover():
                        return
                else:
                    if menu.check_rect(event.pos):
                        reset_game(surface, menu, ttt)
        pygame.display.update()
        fps_clock.tick(fps)

def terminate():
    pygame.quit()
    sys.exit()

def reset_game(surface, menu, ttt):
    surface.fill(white)
    menu.draw_menu()
    ttt.init_game()
    

class TTT(object):
    def __init__(self, surface, menu):
        self.board = [['-' for i in range(3)] for j in range(3)]
        self.coords = []
        self.set_coords()
        self.surface = surface
        self.menu = menu
        pass

    def init_game(self):
        self.draw_line(self.surface)
        self.turn = 'X'
        self.finish = False
        self.init_board()

    def init_board(self):
        for y in range(3):
            for x in range(3):
                self.board[y][x] = '-'

    def set_coords(self):
        for i in range(3):
            for j in range(3):
                coord = left + j * box_size, top + i * box_size
                self.coords.append(coord)

    def get_coord(self, pos):
        for coord in self.coords:
            x, y = coord
            rect = pygame.Rect(x, y, box_size, box_size)
            if(rect.collidepoint(pos)):
                return coord
        return None

    def get_board(self, coord):
        x, y = coord
        x = (x - left) // box_size
        y = (y - top) // box_size
        return x, y

    def is_full(self):
        for y in range(3):
            for x in range(3):
                if self.board[y][x] == '-':
                    return False
        return True

    def is_win(self, player):
        # 가로와 세로  체크
        for y in range(3):
            row, column = 0, 0
            for x in range(3):
                if self.board[y][x] == player:
                    row += 1
                if self.board[x][y] == player:
                    column += 1
            if row == 3 or column == 3:
                return True
            
        # 대각선 체크
        x, row, column = 2, 0, 0
        for y in range(3):
            if self.board[y][y] == player:
                row += 1
            if self.board[y][x] == player:
                column += 1
            x -= 1
        if row == 3 or column == 3:
            return True

        return False

    def check_board(self, pos):
        coord = self.get_coord(pos)
        if not coord:
            return False

        x, y = self.get_board(coord)
        if self.board[y][x] != '-':
            return True
        else:
            return self.draw_shape(x, y)

    def draw_shape(self, x, y):
        self.board[y][x] = self.turn

        if self.is_win(self.turn):
            self.finish = True
            self.menu.show_msg(self.turn)

        x, y = self.get_pixel_coord(x, y)
        if self.turn == 'X':
            self.draw_x(x, y)
            self.turn = 'O'
        else:
            self.draw_o(x, y)
            self.turn = 'X'
        return True
            
    def draw_line(self, surface):
        for i in range(1, 3, 1):
            gap = box_size * i
            pygame.draw.line(surface, black, (left, top + gap), (right, top + gap), 5)
            pygame.draw.line(surface, black, (left + gap, top), (left + gap, down), 5)

    def get_pixel_coord(self, x, y):
        x = left + x * box_size
        y = top + y * box_size
        return x, y

    def draw_o(self, x, y):
        half = box_size // 2
        r = text_size // 2
        pygame.draw.circle(self.surface, blue, (x + half, y + half), r, 5) 

    def draw_x(self, x, y):
        x1, y1 = x + 15, y + 15
        x2, y2 = x1 + text_size, y1 + text_size
        pygame.draw.line(self.surface, blue, (x1, y1), (x2, y2), 7)
        pygame.draw.line(self.surface, blue, (x2, y1), (x1, y2), 7)

    def check_gameover(self):
        if self.is_full():
            if not self.finish:
                self.menu.show_msg('tie')
            self.finish = True
        return self.finish
    

class Menu(object):
    def __init__(self, surface):
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.surface = surface
        self.draw_menu()

    def draw_menu(self):
        x = center_x - width // 4
        self.new_rect = self.make_text('New Game', black, white, x, height - 30)
        x = center_x + width // 4
        self.quit_rect = self.make_text('Quit Game', black, white, x, height - 30)

    def show_msg(self, msg_id):
        msg = {
            'X': 'X player win!',
            'O': 'O player win!',
            'tie': 'Tie',
        }
        self.make_text(msg[msg_id], blue, white, center_x, 30)

    def make_text(self, text, color, bgcolor, cx, cy):
        surf = self.font.render(text, True, color, bgcolor)
        rect = surf.get_rect()
        rect.center = (cx, cy)
        self.surface.blit(surf, rect)
        return rect

    def check_rect(self, pos):
        if self.new_rect.collidepoint(pos):
            return True
        elif self.quit_rect.collidepoint(pos):
            terminate()
        return False

    def is_continue(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                elif event.type == MOUSEBUTTONUP:
                    if (self.check_rect(event.pos)):
                        return
            pygame.display.update()
            fps_clock.tick(fps)
        
        

if __name__ == '__main__':
    main()
