import pygame
import sys
from enum import Enum, auto
import random
import math


# 화면 상태값
class ScreenState(Enum):
    game_start = auto()
    game_main = auto()
    game_retry = auto()
    game_how_to_play = auto()


# 화면 크기
SCREEN_HEIGHT, SCREEN_WIDTH = 800, 800

# 색상 값
COLOR_SKY_BLUE = (0, 128, 128)
COLOR_DARK_BLUE = (0, 64, 64)

pygame.init()


def draw_button(surface, rect, message):
    pygame.draw.rect(surface, COLOR_DARK_BLUE, rect, border_radius=30)
    message = font35.render(message, True, (255, 255, 255))

    pos = list(rect.center)
    pos[1] -= 5
    message_rect = message.get_rect(center=pos)
    surface.blit(message, message_rect)


button_size = 400
button_full_size = SCREEN_WIDTH - 100
start_button = pygame.Rect(SCREEN_WIDTH // 2 - button_size // 2, 400, button_size, 60)
how_to_button = pygame.Rect(SCREEN_WIDTH // 2 - button_size // 2, 400 + 60 + 20, button_size, 60)
back_button = pygame.Rect(SCREEN_WIDTH // 2 - button_full_size // 2, SCREEN_HEIGHT - 80, button_full_size, 60)

clock = pygame.time.Clock()
# fps
FPS = 120

font20 = pygame.font.Font("font/malgun.ttf", 20)
font25 = pygame.font.Font("font/malgun.ttf", 25)
font30 = pygame.font.Font("font/malgun.ttf", 30)
font35 = pygame.font.Font("font/malgun.ttf", 35)
font40 = pygame.font.Font("font/malgun.ttf", 40)
font100 = pygame.font.Font("font/malgun.ttf", 100)

pygame.mixer.music.load("music/dodgeBackground.ogg")
pygame.mixer.music.play(-1)
dodge_icon = pygame.image.load("img/icon.png")
pygame.display.set_icon(dodge_icon)
game_over_audio = pygame.mixer.Sound("music/gameover.wav")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("닷지게임")

me_image_stop = pygame.image.load("img/playerGrey_up1.png")
me_image_stop = pygame.transform.scale(me_image_stop, (me_image_stop.get_width() // 2, me_image_stop.get_height() // 2))
me_image_walk = pygame.image.load("img/playerGrey_up2.png")
me_image_walk = pygame.transform.scale(me_image_walk, (me_image_walk.get_width() // 2, me_image_walk.get_height() // 2))
me = [me_image_stop, me_image_walk]

# me = pygame.transform.scale(me, (54, 67))
me_stop_width, me_stop_height = me[0].get_size()
me_stop_rect = me[0].get_rect()
me_stop_rect.x = SCREEN_WIDTH // 2 - me_stop_width // 2
me_stop_rect.y = SCREEN_HEIGHT // 2 - me_stop_height // 2
me_mask_stop = pygame.mask.from_surface(me[0])

me_move_width, me_move_height = me[1].get_size()
me_move_rect = me[1].get_rect()
me_move_rect.x = SCREEN_WIDTH // 2 - me_move_width // 2
me_move_rect.y = SCREEN_HEIGHT // 2 - me_move_height // 2
me_mask_move = pygame.mask.from_surface(me[1])
# me_color = (255, 255, 0)  # 빨간색
# me_radius = 15  # 동그라미의 반지름
# me_rect = pygame.Rect(SCREEN_WIDTH // 2 - me_radius, SCREEN_HEIGHT // 2 - me_radius, me_radius * 2, me_radius * 2)

me_speed = 2
# 게임 시간
state_game_time = 0
# 게임 레벨
state_game_level = 1
# 레벨 올라 가는 기준
# 2레벨
# 일반 적 레이턴시 감소
# 3레벨
# 새로운 적 (벽튕기기적)
# 4레벨
# 모든적 속도 증가
# 5레벨
# 일반 적 레이턴시 감소
state_game_level_list = [4, 18, 22, 36, 40]
# 일반 적
enemy_size = 6.5
enemy_speed = 1.5
enemies = []
enemies_rect = []
# 벽튕기는 적
hard_enemy_size = 15
hard_enemy_speed = 1.3
hard_enemies = []

# 게임 시간을 측정하기위해 필요한 변수
last_game_time = pygame.time.get_ticks()

# 마지막 적 생성 시간
last_spawn_time = pygame.time.get_ticks()
# 적 생성 시간 간격 설정
spawn_interval = 1000

last_hard_spawn_time = pygame.time.get_ticks()
hard_spawn_interval = 8000
is_show_hard_enemy = False


def draw_enemy(x, y):
    radius = 5
    pygame.draw.circle(screen, (255, 165, 0), [x, y], radius)
    rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
    enemies_rect.append(rect)


def spawn_hard_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        enemy_x = random.randint(0, SCREEN_WIDTH)
        enemy_y = 0
    elif side == "bottom":
        enemy_x = random.randint(0, SCREEN_WIDTH)
        enemy_y = SCREEN_HEIGHT - enemy_size
    elif side == "left":
        enemy_x = 0
        enemy_y = random.randint(0, SCREEN_HEIGHT)
    elif side == "right":
        enemy_x = SCREEN_WIDTH - enemy_size
        enemy_y = random.randint(0, SCREEN_HEIGHT)

    # 적의 초기 방향 설정

    player_direction = [me_stop_rect.x - enemy_x, me_stop_rect.y - enemy_y]
    print(player_direction)
    length = math.sqrt(player_direction[0] ** 2 + player_direction[1] ** 2)
    enemy_direction = [player_direction[0] / length, player_direction[1] / length]
    enemy_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(enemy_surface, (255, 50, 50), (15, 15), enemy_size)
    hard_enemies.append([enemy_x, enemy_y, enemy_direction, enemy_surface])


# 함수 정의
def spawn_enemy():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        enemy_x = random.randint(0, SCREEN_WIDTH)
        enemy_y = 0
    elif side == "bottom":
        enemy_x = random.randint(0, SCREEN_WIDTH)
        enemy_y = SCREEN_HEIGHT - enemy_size
    elif side == "left":
        enemy_x = 0
        enemy_y = random.randint(0, SCREEN_HEIGHT)
    elif side == "right":
        enemy_x = SCREEN_WIDTH - enemy_size
        enemy_y = random.randint(0, SCREEN_HEIGHT)

    # 적의 초기 방향 설정

    player_direction = [me_stop_rect.x - enemy_x, me_stop_rect.y - enemy_y]
    print(player_direction)
    length = math.sqrt(player_direction[0] ** 2 + player_direction[1] ** 2)
    enemy_direction = [player_direction[0] / length, player_direction[1] / length]
    enemy_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(enemy_surface, (255, 165, 0), (15, 15), enemy_size)
    enemies.append([enemy_x, enemy_y, enemy_direction, enemy_surface])


def state_start_game_event(e):
    global state, key_check
    if e.type == pygame.KEYUP:
        key_check = False
    if e.type == pygame.KEYDOWN:
        state = ScreenState.game_main
        key_check = True
    if e.type == pygame.MOUSEBUTTONDOWN:
        print(e.pos)
        if how_to_button.collidepoint(e.pos):
            state = ScreenState.game_how_to_play


def state_main_game_event(e):
    pass


key_check = True


def state_retry_game_event(e):
    global key_check, hard_enemy_size, last_hard_spawn_time, hard_spawn_interval, is_show_hard_enemy, hard_enemy_speed, hard_enemies, state, me_stop_rect, me_speed, state_game_time, state_game_level, enemy_speed, enemies, last_spawn_time, last_game_time, spawn_interval
    if e.type == pygame.KEYUP:
        if key_check:
            key_check = False
    if e.type == pygame.KEYDOWN and not key_check:
        pygame.mixer.music.play(-1)
        state = ScreenState.game_main
        me_stop_rect.x = SCREEN_WIDTH // 2 - me_stop_rect.width
        me_stop_rect.y = SCREEN_HEIGHT // 2 - me_stop_rect.height
        me_move_rect.x = SCREEN_WIDTH // 2 - me_move_rect.width
        me_move_rect.y = SCREEN_HEIGHT // 2 - me_move_rect.height
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
        hard_enemy_size = 15
        hard_enemy_speed = 1.3
        hard_enemies = []

        last_hard_spawn_time = pygame.time.get_ticks()
        hard_spawn_interval = 8000
        is_show_hard_enemy = False


def draw_start_screen():
    screen.fill(COLOR_SKY_BLUE)
    title = font100.render("닷지 게임", True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    sub_title = font30.render("아무키나 눌러 시작해주세요", True, (255, 255, 255))
    screen.blit(sub_title, (SCREEN_WIDTH // 2 - sub_title.get_width() // 2, 200 + title.get_height() + 20))
    draw_button(screen, how_to_button, "게임방법")


def draw_retry_screen():
    pygame.mixer.music.stop()
    screen.fill(COLOR_SKY_BLUE)
    title = font100.render("게임 오버", True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 130))
    any_key_subscription = font30.render("다시 시작하려면 아무 키나 눌러주세요", True, (255, 255, 255))
    screen.blit(any_key_subscription,
                (SCREEN_WIDTH // 2 - any_key_subscription.get_width() // 2 + 20, 130 + title.get_height() + 20))
    sub_title = font25.render("점수", True, (255, 255, 255))
    screen.blit(sub_title,
                (SCREEN_WIDTH // 2 - sub_title.get_width() // 2, SCREEN_HEIGHT // 2 - sub_title.get_height()))
    score = font100.render(f"{state_game_time}", False, (255, 255, 255))
    screen.blit(score,
                (SCREEN_WIDTH // 2 - score.get_width() // 2,
                 SCREEN_HEIGHT // 2 - sub_title.get_height() + sub_title.get_height() + 20))


def convert_time(time):
    minutes = time // 60
    seconds = time % 60
    return f"점수 {time}"


# 걷고 있을 때와 멈춤 상태를 구분하기 위한 변수
walking = False
walking_time = 0
walk_interval = 500

current_image = me[0]


def create_circle_rect(center_x, center_y, radius):
    # 원의 내접 직사각형 계산
    rect = pygame.Rect(center_x - radius, center_y - radius, radius * 2, radius * 2)
    return rect


def draw_how_to_play_screen():
    screen.fill(COLOR_SKY_BLUE)
    header = font100.render("게임 방법", True, (255, 255, 255))
    screen.blit(header, (SCREEN_WIDTH // 2 - header.get_width() // 2, 30))
    me_image = me[0]
    me_image = pygame.transform.scale(me_image, (60, 60))
    screen.blit(me_image, (50, 60 + header.get_height()))
    me_desc1 = font25.render("플레이어의 캐릭터입니다. 방향키로 움직일 수 있고", True, (255, 255, 255))
    me_desc2 = font25.render("총알과 닿았을 때 게임이 종료 됩니다.", True, (255, 255, 255))
    screen.blit(me_desc1, (50 + me_image.get_width() + 50, 60 + header.get_height()))
    screen.blit(me_desc2, (50 + me_image.get_width() + 50, 60 + header.get_height() + me_desc2.get_height()))
    pygame.draw.circle(screen, (255, 165, 0), (50 + 30, 60 + header.get_height() + me_desc2.get_height() + 40 + 50), 30)
    enemy_desc1 = font25.render("기본 총알 : 총알과 닿으면 게임이 종료 됩니다.", True, (255, 255, 255))
    screen.blit(enemy_desc1, (50 + 30 + 50 + 25, 60 + header.get_height() + me_desc2.get_height() + 40 + 30))
    pygame.draw.circle(screen, (255, 50, 0),
                       (50 + 30, 60 + header.get_height() + me_desc2.get_height() + 40 + 50 + 75 + 20), 30)
    hard_enemy_desc1 = font25.render("특수 총알 : 총알과 닿으면 게임이 종료 됩니다.", True, (255, 255, 255))
    hard_enemy_desc2 = font25.render("해당 총알은 벽에 닿아도 튕겨서 다시 돌아옵니다.", True, (255, 255, 255))
    screen.blit(hard_enemy_desc1, (50 + 30 + 50 + 25, 60 + header.get_height() + me_desc2.get_height() + 40 + 110))
    screen.blit(hard_enemy_desc2, (
    50 + 30 + 50 + 25, 60 + header.get_height() + me_desc2.get_height() + 40 + 110 + hard_enemy_desc1.get_height()))
    draw_button(screen, back_button, "돌아가기")
    # 255,50,50


def draw_main_screen():
    global is_show_hard_enemy, hard_enemy_speed, hard_enemy_speed, hard_spawn_interval, last_spawn_time, last_hard_spawn_time, walking, current_image, walking_time, spawn_interval, state, enemy_speed, state_game_level, last_game_time, state_game_time
    screen.fill(COLOR_SKY_BLUE)
    for i in state_game_level_list:
        if i == state_game_time:
            # 레벨 2
            if i == state_game_level_list[0]:
                print("level2")
                enemy_speed += 0.3
                spawn_interval = 800
                state_game_level = 2
                state_game_time += 1
            elif i == state_game_level_list[1]:
                print("level3")
                state_game_level = 3
                enemy_speed += 0.3
                spawn_interval = 700
                state_game_time += 1
                is_show_hard_enemy = True
            elif i == state_game_level_list[2]:
                print("level4")
                spawn_interval = 500
                hard_enemy_speed += 0.3
                state_game_level = 4
                state_game_time += 1
            elif i == state_game_level_list[3]:
                print("level5")
                state_game_level = 5
                hard_enemy_speed += 0.8
                hard_spawn_interval = 2000
                state_game_time += 1
            elif i == state_game_level_list[4]:
                print("level6")
                state_game_level = 6
                state_game_time += 1

    font_game_level = font20.render("점수", True, (255, 255, 255), )

    font_game_time = font25.render(f"{state_game_time}", True, (255, 255, 255), )
    screen.blit(font_game_level,
                (SCREEN_WIDTH // 2 - (font_game_time.get_width() + font_game_level.get_width()) // 2, 4))
    screen.blit(font_game_time,
                (SCREEN_WIDTH // 2 - (font_game_time.get_width()) // 2 + font_game_level.get_width() // 2 + 5, 0))

    # pygame.draw.circle(screen, me_color, me_rect.center, me_radius)
    current_game_time = pygame.time.get_ticks()
    if current_game_time - last_game_time > 1000:
        state_game_time += 1
        last_game_time = current_game_time
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > spawn_interval:
        spawn_enemy()
        last_spawn_time = current_time
    current_hard_time = pygame.time.get_ticks()
    if is_show_hard_enemy and current_hard_time - last_hard_spawn_time > hard_spawn_interval:
        spawn_hard_enemy()
        last_hard_spawn_time = current_hard_time
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        me_stop_rect.x -= me_speed
        me_move_rect.x -= me_speed
        walking = True
        if me_stop_rect.x < 0:
            me_stop_rect.x = 0
            me_move_rect.x = 0
    if keys[pygame.K_RIGHT]:
        me_stop_rect.x += me_speed
        me_move_rect.x += me_speed
        walking = True
        if me_stop_rect.x > SCREEN_WIDTH - me_stop_rect.width:
            me_stop_rect.x = SCREEN_WIDTH - me_stop_rect.width
            me_move_rect.x = SCREEN_WIDTH - me_move_rect.width
    if keys[pygame.K_UP]:
        me_stop_rect.y -= me_speed
        me_move_rect.y -= me_speed
        walking = True
        if me_stop_rect.y < 0:
            me_stop_rect.y = 0
            me_move_rect.y = 0
    if keys[pygame.K_DOWN]:
        me_stop_rect.y += me_speed
        me_move_rect.y += me_speed
        walking = True
        if me_stop_rect.y > SCREEN_HEIGHT - me_stop_rect.height:
            me_stop_rect.y = SCREEN_HEIGHT - me_stop_rect.height
            me_move_rect.y = SCREEN_HEIGHT - me_move_rect.height
    if not any(keys):
        walking = False

    # 걷는 상태이면서 일정 시간이 경과하면 이미지 변경
    if walking and pygame.time.get_ticks() - walking_time > 500:
        walking_time = pygame.time.get_ticks()
        current_image = me[0] if current_image == me[1] else me[1]

    screen.blit(current_image, (me_stop_rect.x, me_stop_rect.y))
    for index, hard_enemy in enumerate(hard_enemies):
        hard_enemy[0] += hard_enemy_speed * hard_enemy[2][0]
        hard_enemy[1] += hard_enemy_speed * hard_enemy[2][1]
        if hard_enemy[0] < 0 or hard_enemy[0] > SCREEN_WIDTH - 15:  # 화면 좌우 벽과의 충돌 확인
            hard_enemy[2][0] *= -1  # x 방향 반전
            # 충돌 후 위치 보정
            hard_enemy[0] = max(0, min(hard_enemy[0], SCREEN_WIDTH - 15))

        if hard_enemy[1] < 0 or hard_enemy[1] > SCREEN_HEIGHT - 15:  # 화면 상하 벽과의 충돌 확인
            hard_enemy[2][1] *= -1  # y 방향 반전
            # 충돌 후 위치 보정
            hard_enemy[1] = max(0, min(hard_enemy[1], SCREEN_HEIGHT - 15))

        rect_mask = pygame.mask.from_surface(hard_enemy[3])
        if current_image == me[0]:
            offset = (hard_enemy[0] - me_stop_rect.x, hard_enemy[1] - me_stop_rect.y)
            if me_mask_stop.overlap(rect_mask, offset):
                # pygame.time.wait(100)
                state = ScreenState.game_retry
                game_over_audio.play()
                pygame.display.flip()
        elif current_image == me[1]:
            offset = (hard_enemy[0] - me_move_rect.x, hard_enemy[1] - me_move_rect.y)
            if me_mask_move.overlap(rect_mask, offset):
                pygame.time.wait(500)
                state = ScreenState.game_retry
                game_over_audio.play()

    # 적 이동 및 생성
    for index, enemy in enumerate(enemies):
        # 적의 이동 방향으로 이동
        enemy[0] += enemy_speed * enemy[2][0]
        enemy[1] += enemy_speed * enemy[2][1]

        rect_mask = pygame.mask.from_surface(enemy[3])
        if current_image == me[0]:
            offset = (enemy[0] - me_stop_rect.x, enemy[1] - me_stop_rect.y)
            if me_mask_stop.overlap(rect_mask, offset):
                game_over_audio.play()
                state = ScreenState.game_retry
                pygame.time.wait(500)
        elif current_image == me[1]:
            offset = (enemy[0] - me_move_rect.x, enemy[1] - me_move_rect.y)
            if me_mask_move.overlap(rect_mask, offset):
                game_over_audio.play()
                state = ScreenState.game_retry
                pygame.time.wait(500)

    for enemy in enemies:
        screen.blit(enemy[3], (enemy[0], enemy[1]))

    for hare_enemy in hard_enemies:
        screen.blit(hare_enemy[3], (hare_enemy[0], hare_enemy[1]))


def state_how_to_play_event(e):
    global state
    if e.type == pygame.MOUSEBUTTONDOWN:
        print(e.pos)
        if back_button.collidepoint(e.pos):
            state = ScreenState.game_start


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
        elif state == ScreenState.game_how_to_play:
            state_how_to_play_event(event)

        # 메인화면 이벤트 처리
        elif state == ScreenState.game_main:
            state_main_game_event(event)
        # 게임 오버 화면 이벤트 처리
        else:
            state_retry_game_event(event)

    if state == ScreenState.game_start:
        draw_start_screen()
    elif state == ScreenState.game_how_to_play:
        draw_how_to_play_screen()
    elif state == ScreenState.game_main:
        draw_main_screen()
    else:
        draw_retry_screen()

    pygame.display.flip()
    clock.tick(FPS)
