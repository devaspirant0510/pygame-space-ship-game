import pygame
import sys

# 초기화 함수 파이게임을 사용하기 위해서 프로그램 최상단에 선언
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("파이게임을 배워보자")

img_path = "img/spaceShip.png"
my_img = pygame.image.load(img_path)
# 이미지 크기 변경
my_img = pygame.transform.scale(my_img,(200,200))
my_img_width,my_img_height = my_img.get_size()
print(my_img_width,my_img_height)



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # # 원 그리기
    # pygame.draw.circle(screen,"red",(130,130),100)
    # # 직사각형 그리기
    # pygame.draw.rect(screen,"blue",(50,250,60,100))
    # # 선 그리기
    # pygame.draw.line(screen,"green",(10,400),(600,300),12)
    screen.blit(my_img,(200,100))
    pygame.display.flip()


sys.exit()