import pygame
import sys
from enum import Enum, auto
import random
import math


class ScreenState(Enum):
    game_start = auto()
    game_main = auto()
    game_retry = auto()


COLOR_SKY = (0, 128, 128)

pygame.init()

clock = pygame.time.Clock()
# fps
FPS = 120

font20 = pygame.font.Font("font/malgun.ttf", 20)
font25 = pygame.font.Font("font/malgun.ttf", 25)
font30 = pygame.font.Font("font/malgun.ttf", 30)
font35 = pygame.font.Font("font/malgun.ttf", 35)
font40 = pygame.font.Font("font/malgun.ttf", 40)

SCREEN_HEIGHT, SCREEN_WIDTH = 800, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("닷지게임")

me_image_stop = pygame.image.load("img/playerGrey_up1.png")
me_image_stop = pygame.transform.scale(me_image_stop, (me_image_stop.get_width() // 2, me_image_stop.get_height() // 2))
me_image_walk = pygame.image.load("img/playerGrey_up2.png")
me_image_walk = pygame.transform.scale(me_image_walk, (me_image_walk.get_width() // 2, me_image_walk.get_height() // 2))
me = [me_image_stop, me_image_walk]

# me = pygame.transform.scale(me, (54, 67))
me_width, me_height = me[0].get_size()
me_rect = me[0].get_rect()
me_rect.x = SCREEN_WIDTH // 2 - me_width // 2
me_rect.y = SCREEN_HEIGHT // 2 - me_height // 2
me_mask = pygame.mask.from_surface(me[0])
# me_color = (255, 255, 0)  # 빨간색
# me_radius = 15  # 동그라미의 반지름
# me_rect = pygame.Rect(SCREEN_WIDTH // 2 - me_radius, SCREEN_HEIGHT // 2 - me_radius, me_radius * 2, me_radius * 2)

me_speed = 2
# 게임 시간
state_game_time = 0
# 게임 레벨
state_game_level = 1
# 레벨올라가는 기준
state_game_level_list = [8, 20, 60, 80, 100]
# 적
enemy_size = 30
enemy_speed = 1.5
enemies = []
enemies_rect = []
# 마지막 적 생성 시간
last_spawn_time = pygame.time.get_ticks()
# 게임 시간을 측정하기위해 필요한 변수
last_game_time = pygame.time.get_ticks()

# 적 생성 시간 간격 설정
spawn_interval = 1000


def draw_enemy(x, y):
    radius = 15
    pygame.draw.circle(screen, (200, 100, 0), [x, y], 15)
    rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
    enemies_rect.append(rect)


# 함수 정의
def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        enemy_x = random.randint(0, SCREEN_WIDTH - enemy_size)
        enemy_y = 0
    elif side == "bottom":
        enemy_x = random.randint(0, SCREEN_WIDTH - enemy_size)
        enemy_y = SCREEN_HEIGHT - enemy_size
    elif side == "left":
        enemy_x = 0
        enemy_y = random.randint(0, SCREEN_HEIGHT - enemy_size)
    elif side == "right":
        enemy_x = SCREEN_WIDTH - enemy_size
        enemy_y = random.randint(0, SCREEN_HEIGHT - enemy_size)

    # 적의 초기 방향 설정

    player_direction = [me_rect.x - enemy_x, me_rect.y - enemy_y]
    print(player_direction)
    length = math.sqrt(player_direction[0] ** 2 + player_direction[1] ** 2)
    enemy_direction = [player_direction[0] / length, player_direction[1] / length]
    enemy_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(enemy_surface, (200, 100, 0), (15, 15), 15)

    enemies.append([enemy_x, enemy_y, enemy_direction, enemy_surface])


def state_start_game_event(e):
    global state
    if e.type == pygame.KEYDOWN:
        state = ScreenState.game_main


def state_main_game_event(e):
    pass


def state_retry_game_event(e):
    global state, me_rect, me_speed, state_game_time, state_game_level, enemy_speed, enemies, last_spawn_time, last_game_time, spawn_interval
    if e.type == pygame.KEYDOWN:
        state = ScreenState.game_main
        me_rect.x = SCREEN_WIDTH // 2 - me_rect.width
        me_rect.y = SCREEN_HEIGHT // 2 - me_rect.height
        me_speed = 2
        # 게임 시간
        state_game_time = 0
        # 게임 레벨
        state_game_level = 1
        # 레벨올라가는 기준
        enemy_speed = 1.5
        enemies = []
        # 마지막 적 생성 시간
        last_spawn_time = pygame.time.get_ticks()
        # 게임 시간을 측정하기위해 필요한 변수
        last_game_time = pygame.time.get_ticks()

        # 적 생성 시간 간격 설정
        spawn_interval = 1000


def draw_start_screen():
    title = font40.render("닷지 게임", True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - title.get_height() // 2))
    sub_title = font25.render("아무키나 눌러 시작해주세요", True, (255, 255, 255))
    screen.blit(sub_title, (SCREEN_WIDTH // 2 - sub_title.get_width() // 2, SCREEN_HEIGHT // 2 + 30))


def draw_retry_screen():
    screen.fill(COLOR_SKY)
    title = font40.render("게임 오버", True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 130))
    any_key_subscription = font30.render("다시 시작하려면 아무 키나 눌러주세요", True, (255, 255, 255))
    screen.blit(any_key_subscription, (SCREEN_WIDTH // 2 - any_key_subscription.get_width() // 2, 180))
    sub_title = font25.render(f"당신의 버틴 시간은... {convert_time(state_game_time)}", True, (255, 255, 255))
    screen.blit(sub_title,
                (SCREEN_WIDTH // 2 - sub_title.get_width() // 2, SCREEN_HEIGHT // 2 - sub_title.get_height()))


def convert_time(time):
    minutes = time // 60
    seconds = time % 60
    return f"{minutes:02d}:{seconds:02d}"


# 걷고 있을 때와 멈춤 상태를 구분하기 위한 변수
walking = False
walking_time = 0
walk_interval = 500

current_image = me[0]


def create_circle_rect(center_x, center_y, radius):
    # 원의 내접 직사각형 계산
    rect = pygame.Rect(center_x - radius, center_y - radius, radius * 2, radius * 2)
    return rect


def draw_main_screen():
    global last_spawn_time, walking, current_image, walking_time, spawn_interval, state, enemy_speed, state_game_level, last_game_time, state_game_time
    screen.fill(COLOR_SKY)
    for i in state_game_level_list:
        # level2
        if i == state_game_time:
            enemy_speed -= 0.1
            state_game_level = 2
            state_game_time += 1
    font_game_level = font20.render(f"레벨 {state_game_level}", True, (255, 255, 255), )
    screen.blit(font_game_level, (5, 0))
    font_game_time = font20.render(f"시간 {convert_time(state_game_time)}", True, (255, 255, 255), )
    screen.blit(font_game_time, (SCREEN_WIDTH - font_game_time.get_width(), 0))

    # pygame.draw.circle(screen, me_color, me_rect.center, me_radius)
    current_game_time = pygame.time.get_ticks()
    if current_game_time - last_game_time > 1000:
        state_game_time += 1
        last_game_time = current_game_time
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > spawn_interval:
        spawn_enemy()
        last_spawn_time = current_time
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        me_rect.x -= me_speed
        walking = False
        if me_rect.x < 0:
            me_rect.x = 0
    if keys[pygame.K_RIGHT]:
        me_rect.x += me_speed
        walking = False
        if me_rect.x > SCREEN_WIDTH - me_rect.width:
            me_rect.x = SCREEN_WIDTH - me_rect.width
    if keys[pygame.K_UP]:
        me_rect.y -= me_speed
        walking = False
        if me_rect.y < 0:
            me_rect.y = 0
    if keys[pygame.K_DOWN]:
        me_rect.y += me_speed
        walking = False
        if me_rect.y > SCREEN_HEIGHT - me_rect.height:
            me_rect.y = SCREEN_HEIGHT - me_rect.height
    if not any(keys):
        walking = False

    screen.blit(current_image, (me_rect.x, me_rect.y))

    # 걷는 상태이면서 일정 시간이 경과하면 이미지 변경
    if walking and pygame.time.get_ticks() - walking_time > 500:
        walking_time = pygame.time.get_ticks()
        current_image = me[0] if current_image == me[1] else me[1]

    # 적 이동 및 생성
    for index, enemy in enumerate(enemies):
        # 적의 이동 방향으로 이동
        enemy[0] += enemy_speed * enemy[2][0]
        enemy[1] += enemy_speed * enemy[2][1]
        # 적의 위치와 벽의 충돌을 확인
        # 적의 위치와 벽의 충돌을 확인
        if enemy[0] < 0 or enemy[0] > SCREEN_WIDTH - 15:  # 화면 좌우 벽과의 충돌 확인
            enemy[2][0] *= -1  # x 방향 반전
            # 충돌 후 위치 보정
            enemy[0] = max(0, min(enemy[0], SCREEN_WIDTH - 15))

        if enemy[1] < 0 or enemy[1] > SCREEN_HEIGHT - 15:  # 화면 상하 벽과의 충돌 확인
            enemy[2][1] *= -1  # y 방향 반전
            # 충돌 후 위치 보정
            enemy[1] = max(0, min(enemy[1], SCREEN_HEIGHT - 15))

        rect_mask = pygame.mask.from_surface(enemy[3])
        offset = (enemy[0] - me_rect.x, enemy[1] - me_rect.y)
        if me_mask.overlap(rect_mask, offset):
            pygame.time.wait(1000)
            state = ScreenState.game_retry

    for enemy in enemies:
        screen.blit(enemy[3], (enemy[0], enemy[1]))


is_running = True
state = ScreenState.game_start

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            sys.exit()
        # 시작화면 이벤트 처리
        if state == ScreenState.game_start:
            state_start_game_event(event)
        # 메인화면 이벤트 처리
        elif state == ScreenState.game_main:
            state_main_game_event(event)
        # 게임 오버 화면 이벤트 처리
        else:
            state_retry_game_event(event)

    if state == ScreenState.game_start:
        draw_start_screen()
    elif state == ScreenState.game_main:
        draw_main_screen()
    else:
        draw_retry_screen()

    pygame.display.flip()
    clock.tick(FPS)
