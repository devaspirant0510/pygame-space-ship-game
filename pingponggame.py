import pygame
import random
from enum import Enum, auto
import math

pygame.init()
# font
font20 = pygame.font.SysFont("나눔고딕보통", 20)
font25 = pygame.font.SysFont("나눔고딕보통", 25)
font30 = pygame.font.SysFont("나눔고딕보통", 30)
font40 = pygame.font.SysFont("나눔고딕보통", 40)
font50 = pygame.font.SysFont("나눔고딕보통", 50)
font80 = pygame.font.SysFont("나눔고딕보통", 80)
font100 = pygame.font.SysFont("나눔고딕보통", 100)

# color
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# screen option
SCREEN_WIDTH, SCREEN_HEIGHT = 1050, 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("핑퐁 게임")

# board info
board_start, board_end, board_top, board_bottom = 10, 1040, 65, 645
board_width, board_height = 1030, 580

# button
button_game_start = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 150)
button_game_reset = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 150)


class ScreenState(Enum):
    game_start = auto()
    game_main = auto()
    game_over = auto()


def event_game_start(e):
    global state
    if e.type == pygame.MOUSEBUTTONDOWN:
        print(e.pos)
        if button_game_start.collidepoint(e.pos):
            state = ScreenState.game_main
            game_start_sound.play()


def event_game_main(e):
    global player_y
    if e.type == pygame.MOUSEMOTION:
        # 마우스 이동 이벤트 에서 마우스의 x 좌표를 플레이어 캐릭터의 x 좌표로 설정
        image_player_rect.y = e.pos[1]-image_player.get_height()//2
        if image_player_rect.y < board_top:
            image_player_rect.y = board_top
        if image_player_rect.y > board_bottom-image_player.get_height():
            image_player_rect.y = board_bottom-image_player.get_height()


def event_game_over(e):
    global state, ball_y,ball_x,state_game_score, ball_speed, ball_speed_x, image_ball_rect, ball_speed_y, ball_angle, player_x, player_y, image_player_rect
    if e.type == pygame.MOUSEBUTTONDOWN:
        if button_game_reset.collidepoint(e.pos):
            state = ScreenState.game_main
            game_start_sound.play()
            state_game_score = 0

            # 초기화
            ball_x = SCREEN_WIDTH // 2
            ball_y = SCREEN_HEIGHT // 2
            ball_speed = 8
            ball_speed_x = random.choice([-ball_speed, ball_speed])
            ball_speed_y = random.choice([-ball_speed, ball_speed])
            ball_angle = math.radians(45)
            image_ball_rect = image_ball.get_rect(center=(ball_x, ball_y))

            player_x = 14
            player_y = SCREEN_HEIGHT // 2
            image_player_rect = image_player.get_rect(center=(player_x, player_y))

def draw_game_start():
    screen.fill(COLOR_BLACK)
    title = font100.render("Ping Pong", True, COLOR_WHITE)
    screen.blit(title, (arrange_center_width(title), arrange_center_height(title) - 100))
    draw_button(screen, button_game_start, "게임 시작")


last_game_time = pygame.time.get_ticks()
state_game_score = 0

level_check_time = pygame.time.get_ticks()

# 상태 업데이트 여부를 체크하는 변수 추가
is_score_updated = False
def draw_game_main():
    global last_game_time, state_game_score,ball_speed,is_score_updated
    screen.fill(COLOR_BLACK)
    pygame.draw.line(screen, COLOR_WHITE, [board_start, board_top], [board_end, board_top], 4)
    pygame.draw.line(screen, COLOR_WHITE, [board_start, board_top + board_height], [board_end, board_top + board_height], 4)
    pygame.draw.line(screen, (255, 0, 0), [board_start, board_top], [board_start, board_top + board_height], 4)
    pygame.draw.line(screen, COLOR_WHITE, [board_end, board_top], [board_end, board_top + board_height], 4)
    pygame.draw.line(screen, COLOR_WHITE, [board_start + board_width//2, board_top], [board_start + board_width//2, board_top + board_height], 4)
    screen.blit(image_player, (image_player_rect.x, image_player_rect.y))
    game_score = font40.render(f"점수 : {state_game_score}", True, (255, 255, 255))
    screen.blit(game_score, (SCREEN_WIDTH // 2 - game_score.get_width() // 2, 10))
    update_ball_position()
    screen.blit(image_ball, image_ball_rect)
    current_game_time = pygame.time.get_ticks()
    if current_game_time - last_game_time > 1000:
        last_game_time = current_game_time


def draw_game_over():
    screen.fill(COLOR_BLACK)
    title = font100.render("Game Over", True, COLOR_WHITE)
    score_header = font40.render("점수",True,COLOR_WHITE)
    score = font80.render(f"{state_game_score}",True,COLOR_WHITE)
    screen.blit(title, (arrange_center_width(title), arrange_center_height(title) - 150))
    screen.blit(score_header,(arrange_center_width(score_header),arrange_center_height(title)-150+title.get_height()+10))
    screen.blit(score,(arrange_center_width(score),arrange_center_height(title)-150+title.get_height()+score_header.get_height()+20))

    draw_button(screen, button_game_reset, "다시하기")


ping_sound = pygame.mixer.Sound("music/ball-table.ogg")
pong_sound = pygame.mixer.Sound("music/ball-paddle.ogg")
game_over_sound = pygame.mixer.Sound("music/game_over_pingpong.mp3")
game_start_sound = pygame.mixer.Sound("music/ping_pong_start.ogg")
# fps
FPS = 60
clock = pygame.time.Clock()

image_board = pygame.image.load("img/Board.png")
image_player = pygame.image.load("img/Player.png")
image_computer = pygame.image.load("img/Computer.png")
image_ball = pygame.image.load("img/Ball.png")
image_ball_effect = pygame.image.load("img/ballMotion.png")

ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_speed = 8
ball_speed_x = random.choice([-ball_speed, ball_speed])  # 랜덤으로 왼쪽 또는 오른쪽으로 시작
ball_speed_y = random.choice([-ball_speed, ball_speed])  # 랜덤으로 왼쪽 또는 오른쪽으로 시작
image_ball_rect = image_ball.get_rect()

player_x = 14
player_y = SCREEN_HEIGHT // 2
image_player_rect = image_player.get_rect()
image_player_rect.y = SCREEN_HEIGHT // 2
image_player_rect.x = player_x

# 초기 각도 및 속도 설정
ball_angle = math.radians(45)  # 45도로 설정

is_running = True

state = ScreenState.game_start


def arrange_center_width(rect):
    return SCREEN_WIDTH // 2 - rect.get_width() // 2


def arrange_center_height(rect):
    return SCREEN_HEIGHT // 2 - rect.get_height() // 2


def update_ball_position():
    global ball_x, ball_y,state_game_score, state, ball_speed_x, ball_speed_y, image_ball_rect, ball_angle, ball_speed
    # 공의 위치 업데이트
    ball_x += ball_speed * math.cos(ball_angle)
    ball_y += ball_speed * math.sin(ball_angle)
    image_ball_rect.center = (ball_x, ball_y)
    # 벽에 닿았을 때 튕기기 처리
    if ball_x >= board_end-8:
        ball_angle = math.pi - ball_angle  # 수평 방향으로 튕기도록 설정
        if random.random() < 0.5:
            pong_sound.play()
        else:
            ping_sound.play()

    # 화면 위나 아래에 닿았을 때 튕기기 처리
    if ball_y <= board_top+4:
        ball_y = board_top+4
        ball_angle = -ball_angle  # 화면 위에 닿았을 때 수직 방향으로 튕기
        if random.random() < 0.5:
            pong_sound.play()
        else:
            ping_sound.play()
    elif ball_y >= board_top + board_height-4:
        ball_y = board_top + board_height-4
        ball_angle = -ball_angle  # 화면 아래에 닿았을 때 수직 방향으로 튕기
        if random.random() < 0.5:
            pong_sound.play()
        else:
            ping_sound.play()

    if ball_x <= board_start:
        print("game over")
        state = ScreenState.game_over
        game_over_sound.play()
    if image_player_rect.x + image_player_rect.width > ball_x and image_player_rect.y <= ball_y <= image_player_rect.height + image_player_rect.y:
        ball_angle = math.pi - ball_angle  # 수평 방향으로 튕기도록 설정
        ball_speed+=1
        state_game_score += 1
        if random.random() < 0.5:
            pong_sound.play()
        else:
            ping_sound.play()
    # rotated_effect = pygame.transform.rotate(image_ball, math.degrees(-ball_angle))  # 효과 이미지 회전
    # effect_rect = rotated_effect.get_rect(center=image_ball_rect.center)
    # screen.blit(rotated_effect, effect_rect.topleft)


def draw_button(surface, rect, message):
    pygame.draw.rect(surface, COLOR_WHITE, rect, border_radius=30)
    message = font30.render(message, True, COLOR_BLACK)
    pos = list(rect.center)
    pos[1] -= 5
    message_rect = message.get_rect(center=pos)
    surface.blit(message, message_rect)


while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if state == ScreenState.game_start:
            event_game_start(event)
        elif state == ScreenState.game_main:
            event_game_main(event)
        else:
            event_game_over(event)

    if state == ScreenState.game_start:
        draw_game_start()
    elif state == ScreenState.game_main:
        draw_game_main()
    else:
        draw_game_over()

    clock.tick(FPS)
    pygame.display.flip()
