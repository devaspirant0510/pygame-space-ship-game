import pygame
from enum import Enum, auto

class ScreenState(Enum):
    game_start = auto()
    game_main = auto()
    game_over = auto()

pygame.init()

SCREEN_WIDTH,SCREEN_HEIGHT = 800,600
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("핑퐁 게임")

print(pygame.font.get_fonts())
font20 = pygame.font.SysFont("나눔고딕보통",20)

is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    t = font20.render("안녕",True,(255,255,255))
    screen.blit(t,(0,0))
    pygame.display.flip()