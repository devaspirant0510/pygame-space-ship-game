import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
start_screen = 1
pending_screen = 2
action_screen = 3
result_screen = 4

click_time = 0
user_click_time = 0
reaction_time = 0
game_screen = start_screen
is_run = True

start_time = pygame.time.get_ticks()
action_time = 0

while is_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_run = False
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_screen == start_screen:
                game_screen = pending_screen
                action_time = random.randint(2000, 5000)
                start_time = pygame.time.get_ticks()
            elif game_screen == action_screen:
                user_click_time = pygame.time.get_ticks()
                reaction_time = user_click_time - click_time
                game_screen = result_screen
            elif game_screen==result_screen:
                # game_screen=start_screen
                pass

    screen.fill((255, 255, 255))

    if game_screen == start_screen:
        font = pygame.font.Font(None, 36)
        text = font.render("Click to start", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
    elif game_screen == pending_screen:
        current_time = pygame.time.get_ticks()
        if current_time - start_time > action_time:
            click_time = pygame.time.get_ticks()
            game_screen = action_screen
    elif game_screen == action_screen:
        screen.fill((0, 255, 0))
    elif game_screen == result_screen:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Your reaction time: {reaction_time} milliseconds", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)
