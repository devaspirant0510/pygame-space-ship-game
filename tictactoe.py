import pygame
import sys

# 초기화
pygame.init()

# 화면 설정
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("틱택토 게임")

# 색깔 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LINE_COLOR = (0, 0, 0)

# 게임 보드 초기화
board = [['' for _ in range(3)] for _ in range(3)]

# 현재 차례 설정
current_player = 'X'

# 게임 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // (height // 3)
            clicked_col = mouseX // (width // 3)

            if board[clicked_row][clicked_col] == '':
                board[clicked_row][clicked_col] = current_player

                # 차례 변경
                if current_player == 'X':
                    current_player = 'O'
                else:
                    current_player = 'X'

    # 화면 초기화
    screen.fill(WHITE)

    # 가로 선 그리기
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, i * height // 3), (width, i * height // 3), 5)

    # 세로 선 그리기
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (i * width // 3, 0), (i * width // 3, height), 5)

    # 현재 게임 보드 상태 그리기
    font = pygame.font.Font(None, 100)
    for row in range(3):
        for col in range(3):
            cell_value = board[row][col]
            if cell_value != '':
                if cell_value=='O':
                    text = font.render(cell_value, True, BLUE)
                    text_rect = text.get_rect(center=(col * width // 3 + width // 6, row * height // 3 + height // 6))
                    screen.blit(text, text_rect)
                else:
                    text = font.render(cell_value, True, RED)
                    text_rect = text.get_rect(center=(col * width // 3 + width // 6, row * height // 3 + height // 6))
                    screen.blit(text, text_rect)



    # 화면 업데이트
    pygame.display.flip()
