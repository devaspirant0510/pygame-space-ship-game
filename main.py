import os

import pygame
import random

# pygame initialize
pygame.init()

# music
music_path = os.path.join(os.path.abspath("music"), "music.mp3")
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

laser = pygame.mixer.Sound(os.path.join(os.path.abspath('music'), 'sfx_laser2.ogg'))
button_click = pygame.mixer.Sound(os.path.join(os.path.abspath('music'), 'sfx_twoTone.ogg'))
lose_sound = pygame.mixer.Sound(os.path.join(os.path.abspath('music'), 'sfx_lose.ogg'))
explosion_sound = pygame.mixer.Sound(os.path.join(os.path.abspath('music'), 'explosion.ogg'))

lose_sound.play()
# image path
background_img_path = os.path.join(os.path.abspath("img"), "game_start_screen.png")
start_screen_img = pygame.image.load(background_img_path)
start_screen_img = pygame.transform.scale(start_screen_img, (500, 800))

background_img = os.path.join(os.path.abspath("img"), "background.png")
background_img = pygame.image.load(background_img)

space_ship_img = os.path.join(os.path.abspath("img"), "spaceShip.png")
space_ship_img = pygame.image.load(space_ship_img)
space_ship_img = pygame.transform.scale(space_ship_img, (50, 50))
_, _, space_ship_width, space_ship_height = space_ship_img.get_rect()
space_ship_rect = space_ship_img.get_rect()

missile_img = os.path.join(os.path.abspath("img"), "laserBlue.png")
missile_img = pygame.image.load(missile_img)
missile_img1 = missile_img
missile_img = pygame.transform.scale(missile_img, (6, 30))
_, _, missile_width, missile_height = missile_img.get_rect()
missile_rect = missile_img.get_rect()

explosion = os.path.join(os.path.abspath('img'), 'laserBlue10.png')
explosion_img = pygame.image.load(explosion)
_, _, explosion_width, explosion_height = explosion_img.get_rect()

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

# game start button
rect_width, rect_height = 160, 60
rect_x, rect_y = (width - rect_width) // 2, (height - rect_height) // 2
rect_area = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
space_ship_rect.x = width // 2 - space_ship_width // 2
space_ship_rect.y = 700

# 적 생성 시간 간격 설정
spawn_interval = 2000  # milliseconds (2초마다 적 생성)

# 마지막 적 생성 시간
last_spawn_time = pygame.time.get_ticks()

enemies = []
enemy_speed = 3
enemy_max_count = 1
score = 0
last_score_update = pygame.time.get_ticks()

game_state_start = 1
game_state_main = 2
game_state_over = 3

is_shot = False


# 메인 화면
def main_screen():
    global is_shot, missile_img2, missile_img, player_speed, spawn_interval, score, last_score_update, enemy_speed, enemy_max_count, game_state, space_ship_rect
    if score % 100 == 0:
        enemy_speed += 0.1
        spawn_interval -= 0.05
        player_speed += 0.08
    if score > 400:
        missile_img = missile_img2
    for m in missile:
        # y 축감소
        # print("business")
        m[1] -= missile_speed
        if m[1] < 0:
            missile.remove(m)

    screen.fill((0, 0, 0))
    for y in range(height // background_img.get_rect().height + 1):
        for x in range(width // background_img.get_rect().width + 1):
            screen.blit(background_img, (x * 256, y * 256, 256, 256))

    if 0 > space_ship_rect.x:
        space_ship_rect.x = -5
    if space_ship_rect.x > width - space_ship_width:
        space_ship_rect.x = width - space_ship_width
    if 0 > space_ship_rect.y:
        space_ship_rect.y = y
    if space_ship_rect.y > height - space_ship_height:
        space_ship_rect.y = height - space_ship_height

    for mi in missile:
        for en in enemies:
            if en[0] < mi[0] < en[0] + enemy_width and en[1] + enemy_height > mi[1]:
                screen.blit(explosion_img, (mi[0] - explosion_width // 2, mi[1] - explosion_height // 2))
                explosion_sound.play()
                enemies.remove(en)
                missile.remove(mi)
                score += 10
        screen.blit(missile_img, mi)
    for e in enemies:
        e[1] += enemy_speed
        screen.blit(enemy_img, e)

    for en in enemies:
        if en[1] > 800:
            game_state = game_state_over
        if space_ship_rect.colliderect((en[0], en[1], enemy_width, enemy_height)):
            game_state = game_state_over

    my_score = font.render(f"score: {score}", True, (255, 255, 255))
    screen.blit(my_score, (0, 0))
    # 현재 시간 가져오기
    current_my_time = pygame.time.get_ticks()

    # 1초가 지날 때마다 스코어 증가
    if current_my_time - last_score_update >= 200:
        score += 1
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
                button_click.play()
        elif game_state == game_state_main:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    laser.play()
                    if len(missile) < max_count:
                        missile.append(
                            [space_ship_rect.x + space_ship_width // 2 - missile_width // 2, space_ship_rect.y])
        else:
            if event.type == pygame.KEYDOWN:
                game_state = game_state_start
    if game_state == game_state_start:
        score = 0
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
        lose_sound.play()
        screen.fill((0, 0, 0))
        game_over_message = font.render(f"game Over ", True, (255, 255, 255))
        my_score = font.render(f"myScore :{score}", True, (255, 255, 255))
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
