import random
from os import listdir

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

display_info = pygame.display.Info()

# screen = width, height = 800, 600
screen = width, height = display_info.current_w - 20, display_info.current_h - 100

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

bg = pygame.transform.scale(pygame.image.load(
    './img/background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 2

# player = pygame.Surface(player_size)
# player.fill(WHITE)

player_imgs = [pygame.image.load(
    './animation/' + file).convert_alpha() for file in listdir('./animation')]
player = player_imgs[0]
# player_size = (20, 20)
player_rect = player.get_rect()
player_speed = 8

img_index = 0

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)


def create_enemy():
    # enemy = pygame.Surface((20, 20))
    # enemy.fill(RED)
    # enemy = pygame.image.load('./img/enemy.png').convert_alpha()
    enemy = pygame.transform.scale(
        (pygame.image.load('./img/enemy.png').convert_alpha()), (90, 40))
    enemy_rect = pygame.Rect(
        width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(12, 15)
    return [enemy, enemy_rect, enemy_speed]

k = 2500

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, k)

enemies = []


def create_bonus():
    # bonus = pygame.Surface((20, 20))
    # bonus.fill(GREEN)
    bonus = pygame.transform.scale(
        (pygame.image.load('./img/bonus.png').convert_alpha()), (80, 140))
    bonus_rect = pygame.Rect(random.randint(
        0, width), 0 - bonus.get_height(), *bonus.get_size())
    bonus_speed = random.randint(3, 6)
    return [bonus, bonus_rect, bonus_speed]


CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3500)

bonuses = []

scores = 0

is_working = True

prew_scores = 0

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[K_DOWN] and player_rect.bottom < height:
        player_rect = player_rect.move(0, player_speed)
    if pressed_keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(0, -player_speed)
    if pressed_keys[K_RIGHT] and player_rect.right < width:
        player_rect = player_rect.move(player_speed, 0)
    if pressed_keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(-player_speed, 0)

    # main_surface.blit(bg, (0, 0))

    bgX -= bg_speed
    bgX2 -= bg_speed

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    if bgX < -bg.get_width():
        bgX = bg.get_width()
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(player, player_rect)

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom > height:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            is_working = False

    if scores - prew_scores >= 1:
        prew_scores = scores
        if k > 300:
            k -= 200
        CREATE_ENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(CREATE_ENEMY, k)

    main_surface.blit(font.render(str(scores), True, BLACK), (width - 50, 20))

    pygame.display.flip()

font = pygame.font.SysFont('Verdana', 40)
main_surface.blit(font.render('Ви програли!', True, RED), (width/2 - 100, height/2 - 50))

pygame.display.flip()

is_working = True

while is_working:
    FPS.tick(1200)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
