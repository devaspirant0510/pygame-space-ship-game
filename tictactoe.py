import pygame
import random

# 파이 게임 초기화
pygame.init()
# 텍스트 출력을 위한 폰트 설정
font = pygame.font.SysFont("consolas", 30)
font50 = pygame.font.SysFont("consolas", 40)
font80 = pygame.font.SysFont("consolas", 60)
font100 = pygame.font.SysFont("consolas", 80)

# 타일 크기
tile_size = 200
title_height = 120
footer_height = 130
# 화면 사이즈
screen = pygame.display.set_mode((tile_size * 3, tile_size * 3 + title_height + footer_height))
pygame.display.set_caption("틱택토")
# 아이콘 지정
icon = pygame.image.load("../img/tic-tac-toe.png")
pygame.display.set_icon(icon)

# x 이미지 로드 및 사이즈 변경
image_x = pygame.image.load("img/crossed.png")
image_x = pygame.transform.scale(image_x, (tile_size, tile_size))

# o 이미지 로드 및 사이즈 변경
image_o = pygame.image.load("img/o.png")
image_o = pygame.transform.scale(image_o, (tile_size * 0.87, tile_size * 0.83))

# 3x3 보드
board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# 유저 선공 여부
user_turn = True
# 승리  패배 수
win_count = 0
lose_count = 0

bot_delay = random.randint(700, 1000)  # 봇이 말을 놓는 딜레이 시간 (밀리초)

# 파이게임 기본 폰트 제공 여부
print(pygame.font.get_fonts())

# 사용자 정의 이벤트 생성
BOT_PLAY = pygame.USEREVENT + 1
first_turn = True
game_end = False

# 승리 여부 계산
def evaluate(board):
    for i in range(3):
        if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] != 0:
            return board[i * 3]
        if board[i] == board[i + 3] == board[i + 6] != 0:
            return board[i]
    if board[0] == board[4] == board[8] != 0 or board[2] == board[4] == board[6] != 0:
        return board[4]
    if 0 not in board:
        return 0
    return None  # 게임이 아직 진행 중인 경우


def minimax(board, depth, is_maximizing):
    result = evaluate(board)
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
            if board[i] == 0:
                board[i] = -1
                score = minimax(board, depth + 1, False)
                board[i] = 0
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == 0:
                board[i] = 1
                score = minimax(board, depth + 1, True)
                board[i] = 0
                best_score = min(score, best_score)
        return best_score


def draw_board():
    screen.fill((255, 255, 255))  # 화면을 흰색으로 채우기
    # 승/패 표시 텍스트
    player_info = font.render("win", True, (255, 0, 0))
    player_count = font100.render(f"{win_count}", True, (255, 0, 0))
    screen.blit(player_info, (tile_size // 2 - player_info.get_width() // 2, 5 + title_height + tile_size * 3))
    screen.blit(player_count, (
        tile_size // 2 - player_count.get_width() // 2, title_height + tile_size * 3 + 30))
   
    com_info = font.render("lose", True, (0, 0, 255))
    com_win_count = font100.render(f"{lose_count}", True, (0, 0, 255))
    screen.blit(com_info,
                (tile_size * 2 + tile_size // 2 - com_info.get_width() // 2, 5 + title_height + tile_size * 3))
    screen.blit(com_win_count,
                (tile_size * 2 + tile_size // 2 - com_win_count.get_width() // 2,
                 30 + title_height + tile_size * 3))

    turn = font80.render("Tic Tac Toe", True, (30, 200, 200))
    if user_turn:
        is_player_turn = font.render("player Turn", True, (30, 30, 30))
        resize_turn_icon = pygame.transform.scale(image_o,
                                                  (is_player_turn.get_height(), is_player_turn.get_height()))

    else:
        is_player_turn = font.render("computer Turn", True, (30, 30, 30))
        resize_turn_icon = pygame.transform.scale(image_x,
                                                  (is_player_turn.get_height(), is_player_turn.get_height()))


    screen.blit(turn, (tile_size * 3 // 2 - turn.get_width() // 2, 10))
    screen.blit(is_player_turn, (tile_size * 3 // 2 - is_player_turn.get_width() // 2, 10 + turn.get_height() + 5))
    screen.blit(resize_turn_icon, (
        tile_size * 3 // 2 - is_player_turn.get_width() // 2 - resize_turn_icon.get_width() - 6,
        10 + turn.get_height() + 5))

    # 게임 보드 그리기
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, (100, 100, 100),
                             pygame.Rect(j * tile_size, i * tile_size + title_height, tile_size, tile_size), 3,
                             border_radius=3)
            if board[i * 3 + j] != 0:
                if board[i * 3 + j] == 1:
                    screen.blit(image_o, (j * tile_size + ((tile_size - image_o.get_width()) // 2),
                                          (i * tile_size + ((tile_size - image_o.get_height()) // 2)) + title_height))
                else:
                    screen.blit(image_x, (j * tile_size + ((tile_size - image_x.get_width()) // 2),
                                          (i * tile_size + ((tile_size - image_x.get_height()) // 2)) + title_height))


def check_win():
    # 가로, 세로, 대각선 방향으로 승리 조건 확인
    for i in range(3):
        if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] != 0:
            return board[i * 3]
        if board[i] == board[i + 3] == board[i + 6] != 0:
            return board[i]
    if board[0] == board[4] == board[8] != 0 or board[2] == board[4] == board[6] != 0:
        return board[4]
    # 보드가 다 찼는지 확인
    if 0 not in board:
        return 999  # 무승부
    return 0  # 게임 진행 중


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
    win_status = check_win()
    if win_status != 0:
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
        elif win_status == 999:
            draw_count += 1
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        first_turn = not first_turn  # 게임이 끝날 때마다 턴 변경
        user_turn = first_turn
        if not user_turn:  # 봇의 차례일 때 봇이 말을 놓음
            pygame.time.set_timer(BOT_PLAY, bot_delay)
        game_end = False
    pygame.display.flip()

pygame.quit()
