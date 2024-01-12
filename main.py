import os

import pygame
import random

# pygame initialize
pygame.init()

# 배경음악
music_path = os.path.join(os.path.abspath("music"), "music.mp3")
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# 효과음
sound_laser = pygame.mixer.Sound(os.path.join(os.path.abspath('music'), 'sfx_laser2.ogg'))
sound_click = pygame.mixer.Sound(os.path.join(os.path.abspath('music'), 'sfx_twoTone.ogg'))
sound_lose = pygame.mixer.Sound(os.path.join(os.path.abspath('music'), 'sfx_lose.ogg'))
sound_explosion = pygame.mixer.Sound(os.path.join(os.path.abspath('music'), 'explosion.ogg'))

# 이미지
start_screen_img = os.path.join(os.path.abspath("img"), "game_start_screen.png")
start_screen_img = pygame.image.load(start_screen_img)
start_screen_img = pygame.transform.scale(start_screen_img, (500, 800))  # 이미지 크기 화면 크기에 맞게 변경

background_img = os.path.join(os.path.abspath("img"), "background.png")
background_img = pygame.image.load(background_img)

space_ship_img = os.path.join(os.path.abspath("img"), "spaceShip.png")
space_ship_img = pygame.image.load(space_ship_img)
space_ship_img = pygame.transform.scale(space_ship_img, (50, 50))
space_ship_width, space_ship_height = space_ship_img.get_size()
space_ship_rect = space_ship_img.get_rect()

missile_img = os.path.join(os.path.abspath("img"), "laserBlue.png")
missile_img = pygame.image.load(missile_img)
missile_img1 = missile_img
missile_img = pygame.transform.scale(missile_img, (6, 30))
_, _, missile_width, missile_height = missile_img.get_rect()
missile_rect = missile_img.get_rect()

explosion = os.path.join(os.path.abspath('img'), 'laserBlue10.png')
explosion_img = pygame.image.load(explosion)
explosion_width, explosion_height = explosion_img.get_size()

missile_img2 = os.path.join(os.path.abspath("img"), "laserBlue01.png")
missile_img2 = pygame.image.load(missile_img2)

enemy_img = os.path.join(os.path.abspath("img"), "enemy1.png")
enemy_img = pygame.image.load(enemy_img)
enemy_img = pygame.transform.scale(enemy_img, (65, 65))
_, _, enemy_width, enemy_height = enemy_img.get_rect()
enemy_rect = enemy_img.get_rect()

# screen size
height, width = 800, 500

# 색깔 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
# is game played state
running = True
# fps
FPS = 60
# font
font = pygame.font.Font("font/kenvector_future.ttf", 25)
default_font = pygame.font.Font(None, 25)

# 우주선 위치 초기화
space_ship_rect.x = width // 2 - space_ship_width // 2
space_ship_rect.y = 700

# 적 생성 시간 간격 설정
spawn_interval = 2000  # milliseconds (2초마다 적 생성)

# 마지막 적 생성 시간
last_spawn_time = pygame.time.get_ticks()

# 적 정보
enemies = []
enemy_speed = 3
last_score_update = pygame.time.get_ticks()

game_score = 0

game_state_start = 1
game_state_main = 2
game_state_game_over = 3

is_shot = False


# 메인 화면
def main_screen():
    global is_shot, missile_img2, missile_img, player_speed, spawn_interval, game_score, last_score_update, enemy_speed, enemy_max_count, game_state, space_ship_rect
    # 배경 화면 렌더링
    for y in range(height // background_img.get_rect().height + 1):
        for x in range(width // background_img.get_rect().width + 1):
            screen.blit(background_img, (x * 256, y * 256, 256, 256))

    # 게임 스코어 처리 100의 배수마다 적속도,플레이어 속도 증가, 적 스폰되는 레이턴시 감소
    if game_score % 100 == 0:
        enemy_speed += 0.1
        spawn_interval -= 0.05
        player_speed += 0.08
    # 게임 스코어 400점 이상부터는 missile img 변경
    if game_score > 400:
        missile_img = missile_img2
    # missile 좌표축 변경 매 루프마다 missile_speed 거리만큼 상승함
    for m in missile:
        m[1] -= missile_speed
        if m[1] < 0:
            missile.remove(m)

    # 우주선 벽 밖으로 나가는 처리
    if 0 > space_ship_rect.x:
        space_ship_rect.x = -5
    if space_ship_rect.x > width - space_ship_width:
        space_ship_rect.x = width - space_ship_width
    if 0 > space_ship_rect.y:
        space_ship_rect.y = 0
    if space_ship_rect.y > height - space_ship_height:
        space_ship_rect.y = height - space_ship_height

    # 매 미사일마다 적이랑 닿았는지 확인
    for mi in missile:
        for en in enemies:
            # 만약 닿았다면
            if en[0] < mi[0] < en[0] + enemy_width and en[1] + enemy_height > mi[1]:
                # 폭발 이미지
                screen.blit(explosion_img, (mi[0] - explosion_width // 2, mi[1] - explosion_height // 2))
                # 폭발 효과음 재생
                sound_explosion.play()
                # 적삭제
                enemies.remove(en)
                # 미사일 삭제
                missile.remove(mi)
                # 스코어 증가
                game_score += 20
        # 미사일 이미지 렌더링
        screen.blit(missile_img, mi)
    for e in enemies:
        e[1] += enemy_speed
        screen.blit(enemy_img, e)

    for en in enemies:
        if en[1] > 800:
            game_state = game_state_game_over
        if space_ship_rect.colliderect((en[0], en[1], enemy_width, enemy_height)):
            game_state = game_state_game_over

    my_score = font.render(f"score: {game_score}", True, (255, 255, 255))
    screen.blit(my_score, (0, 0))
    # 현재 시간 가져오기
    current_my_time = pygame.time.get_ticks()

    # 1초가 지날 때마다 스코어 증가
    if current_my_time - last_score_update >= 200:
        game_score += 1
        last_score_update = current_my_time
    screen.blit(space_ship_img, space_ship_rect)


start_screen_mode = True
game_state = game_state_start
player_speed = 5
missile = []
missile_speed = 8
max_count = 5

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == game_state_start:
            if event.type == pygame.KEYDOWN:
                game_state = game_state_main
                sound_click.play()
        elif game_state == game_state_main:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    sound_laser.play()
                    if len(missile) < max_count:
                        missile.append(
                            [space_ship_rect.x + space_ship_width // 2 - missile_width // 2, space_ship_rect.y])
        else:
            if event.type == pygame.KEYDOWN:
                game_state = game_state_start
    if game_state == game_state_start:
        game_score = 0
        game_over_message = font.render(f"press any key to start", True, (255, 255, 255))
        screen.blit(start_screen_img, (0, 0))
        screen.blit(game_over_message, (0, 0))
    elif game_state == game_state_main:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            space_ship_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            space_ship_rect.x += player_speed
        if keys[pygame.K_UP]:
            space_ship_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            space_ship_rect.y += player_speed

            # 현재 시간과 마지막 적 생성 시간 비교하여 일정 시간마다 적 생성
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > spawn_interval:
            new_enemy = [random.randint(0, width // enemy_width) * enemy_width, random.randint(0, 100)]
            enemies.append(new_enemy)
            last_spawn_time = current_time  # 적 생성 시간 갱신
        main_screen()
    else:
        sound_lose.play()
        screen.fill((0, 0, 0))
        game_over_message = font.render(f"game Over ", True, (255, 255, 255))
        my_score = font.render(f"myScore :{game_score}", True, (255, 255, 255))
        any_key = font.render(f"press any key to re-start", True, (255, 255, 255))
        screen.blit(game_over_message, (0, 0))
        screen.blit(my_score, (0, 30))
        screen.blit(any_key, (0, 60))
        missile = []
        enemies = []

        spawn_interval = 2000
        space_ship_rect.x = width // 2 - space_ship_width // 2
        space_ship_rect.y = 700
        enemy_speed = 3
        missile_img = missile_img1

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
