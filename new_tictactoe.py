from typing import Any

import pygame
import random

# Pygame 초기화
pygame.init()

print(pygame.font.get_fonts())

# 텍스트 출력을 위한 폰트 설정
font = pygame.font.SysFont("consolas", 30)
font50 = pygame.font.SysFont("consolas", 40)
font80 = pygame.font.SysFont("consolas", 60)
font100 = pygame.font.SysFont("consolas", 80)

# 타일 크기 및 화면 사이즈 설정
tile_size = 200
title_height = 120
footer_height = 130
screen = pygame.display.set_mode((tile_size * 3, tile_size * 3 + title_height + footer_height))
pygame.display.set_caption("틱택토")
icon = pygame.image.load("../img/tic-tac-toe.png")
pygame.display.set_icon(icon)

# X 이미지 및 O 이미지 로드
image_x = pygame.transform.scale(pygame.image.load("img/crossed.png"), (tile_size, tile_size))
image_o = pygame.transform.scale(pygame.image.load("img/o.png"), (int(tile_size * 0.87), int(tile_size * 0.83)))

# 보드 초기화
board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# 유저 선공 여부 및 승/패 횟수 초기화
user_turn = True
win_count = 0
lose_count = 0
draw_count = 0

# 봇 딜레이 설정
bot_delay = random.randint(700, 1000)

# 사용자 정의 이벤트 생성
BOT_PLAY = pygame.USEREVENT + 1
first_turn = True
game_end = False


# 승리 여부 계산 함수
def evaluate(board_):
    for i in range(3):
        if board_[i * 3] == board_[i * 3 + 1] == board_[i * 3 + 2] != 0:
            return board_[i * 3]
        if board_[i] == board_[i + 3] == board_[i + 6] != 0:
            return board_[i]
    if board_[0] == board_[4] == board_[8] != 0 or board_[2] == board_[4] == board_[6] != 0:
        return board_[4]
    if 0 not in board_:
        return 0
    return None  # 게임이 아직 진행 중인 경우


# 승리 여부 계산 함수
def check_win(board_):
    """
    게임 보드를 평가하여 현재 상태를 반환합니다.

    Parameters:
    - board_: 현재 게임 보드

    Returns:
    - 1: 플레이어가 이긴 경우
    - -1: 컴퓨터가 이긴 경우
    - 0: 무승부
    - None: 게임이 아직 진행 중인 경우
    """
    for i in range(3):
        if board_[i * 3] == board_[i * 3 + 1] == board_[i * 3 + 2] != 0:
            return board_[i * 3]
        if board_[i] == board_[i + 3] == board_[i + 6] != 0:
            return board_[i]
    if board_[0] == board_[4] == board_[8] != 0 or board_[2] == board_[4] == board_[6] != 0:
        return board_[4]
    if 0 not in board_:
        return 0
    return None  # 게임이 아직 진행 중인 경우


# 미니맥스 알고리즘 함수
def minimax(board_, depth, is_maximizing):
    """
    미니맥스 알고리즘을 사용하여 최적의 수를 찾아냅니다.

    Parameters:
    - board_: 현재 게임 보드
    - depth: 현재 탐색 깊이
    - is_maximizing: 최적의 수를 찾을 플레이어인지 여부

    Returns:
    - 최적의 수를 평가한 점수
    """
    result = check_win(board_)
    if result is not None:
        if result == 1:
            return -1
        elif result == -1:
            return 1
        else:
            return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board_[i] == 0:
                board_[i] = -1
                score = minimax(board_, depth + 1, False)
                board_[i] = 0
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board_[i] == 0:
                board_[i] = 1
                score = minimax(board_, depth + 1, True)
                board_[i] = 0
                best_score = min(score, best_score)
        return best_score

# 게임 보드를 그리는 함수
def draw_board():
    # 화면을 흰색으로 채우기
    screen.fill((255, 255, 255))

    # 플레이어와 컴퓨터의 승/패 정보 표시
    player_info = font.render("win", True, (255, 0, 0))
    player_count = font100.render(f"{win_count}", True, (255, 0, 0))
    screen.blit(player_info, (tile_size // 2 - player_info.get_width() // 2, 5 + title_height + tile_size * 3))
    screen.blit(player_count, (tile_size // 2 - player_count.get_width() // 2, title_height + tile_size * 3 + 30))

    com_info = font.render("lose", True, (0, 0, 255))
    com_win_count = font100.render(f"{lose_count}", True, (0, 0, 255))
    screen.blit(com_info, (tile_size * 2 + tile_size // 2 - com_info.get_width() // 2, 5 + title_height + tile_size * 3))
    screen.blit(com_win_count, (tile_size * 2 + tile_size // 2 - com_win_count.get_width() // 2,
                                30 + title_height + tile_size * 3))

    # 게임 타이틀 및 턴 정보 표시
    game_title = font80.render("Tic Tac Toe", True, (30, 200, 200))
    if user_turn:
        is_player_turn = font.render("player Turn", True, (30, 30, 30))
        turn_icon = pygame.transform.scale(image_o, (is_player_turn.get_height(), is_player_turn.get_height()))
    else:
        is_player_turn = font.render("computer Turn", True, (30, 30, 30))
        turn_icon = pygame.transform.scale(image_x, (is_player_turn.get_height(), is_player_turn.get_height()))

    screen.blit(game_title, (tile_size * 3 // 2 - game_title.get_width() // 2, 10))
    screen.blit(is_player_turn, (tile_size * 3 // 2 - is_player_turn.get_width() // 2, 10 + game_title.get_height() + 5))
    screen.blit(turn_icon, (tile_size * 3 // 2 - is_player_turn.get_width() // 2 - turn_icon.get_width() - 6,
                            10 + game_title.get_height() + 5))

    # 게임 보드 그리기
    for y in range(3):
        for x in range(3):
            # 각 타일을 그리고, 비어있는 경우는 그냥 넘어감
            tile_rect = pygame.Rect(x * tile_size, y * tile_size + title_height, tile_size, tile_size)
            pygame.draw.rect(screen, (100, 100, 100), tile_rect, 3, border_radius=3)

            if board[y * 3 + x] != 0:
                # 비어있지 않은 경우에는 X 또는 O 이미지를 해당 위치에 그림
                image = image_o if board[y * 3 + x] == 1 else image_x
                screen.blit(image, (x * tile_size + (tile_size - image.get_width()) // 2,
                                    y * tile_size + (tile_size - image.get_height()) // 2 + title_height))



# 게임 루프
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.MOUSEBUTTONDOWN and user_turn and not game_end:
            x, y = event.pos
            if title_height < y < title_height + tile_size * 3:
                index = (y - title_height) // tile_size * 3 + x // tile_size
                print(x, y, index)
                if board[index] == 0:
                    board[index] = 1
                    user_turn = False
                    pygame.time.set_timer(BOT_PLAY, bot_delay)  # 봇 플레이 이벤트 설정
        if event.type == BOT_PLAY:
            # 한번 호출 후에 비활성화
            pygame.time.set_timer(BOT_PLAY, 0)
            best_score = -float('inf')
            move = None
            for i in range(9):
                if board[i] == 0:
                    board[i] = -1
                    score = minimax(board, 0, False)
                    board[i] = 0
                    if score > best_score:
                        best_score = score
                        move = i

            board[move] = -1
            user_turn = True

    draw_board()
    win_status = check_win(board)
    if win_status != None:
        game_end = True
        s = pygame.Surface((tile_size * 3, tile_size - 40))
        s.set_alpha(80)
        s.fill((0, 0, 0))
        screen.blit(s, (0, title_height + tile_size + 20,))
        if win_status == 1:
            message = "you win!"
        elif win_status == -1:
            message = "you lose..."
        else:
            message = "draw"

        pygame.display.flip()
        turn = font100.render(message, True, (255, 255, 255))
        screen.blit(turn, (tile_size * 3 // 2 - turn.get_width() // 2, (title_height + tile_size * 3 + 50) // 2))
        pygame.display.flip()
        pygame.time.wait(1000)
        if win_status == 1:
            win_count += 1
        elif win_status == -1:
            lose_count += 1
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        first_turn = not first_turn  # 게임이 끝날 때마다 턴 변경
        user_turn = first_turn
        if not user_turn:  # 봇의 차례일 때 봇이 말을 놓음
            pygame.time.set_timer(BOT_PLAY, bot_delay)
        game_end = False
    pygame.display.flip()

pygame.quit()
