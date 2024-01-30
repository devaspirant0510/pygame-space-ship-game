import pygame
import sys

# 초기화 함수 파이게임을 사용하기 위해서 프로그램 최상단에 선언
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("파이게임을 배워보자")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 122, 25))
    pygame.display.flip()


sys.exit()
