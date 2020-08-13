import pygame
import random
import numpy as np
from pygame import mixer

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship logo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("spaceship.png")
player_coordX = 370
player_coordY = 480
player_coordX_dx = 7  # speed of horizontal movement


def player(x, y):
    screen.blit(playerImg, (x, y))


# Monster
monsterImg = []
monster_coordX = []
monster_coordY = []
monster_coordX_dx = []
monster_coordY_dy = []
n_monsters = 6
tuple = (1, -1)  # used to determine random initial direction (verse) of a monster's movement
random_directions = []

for i in range(n_monsters):
    monsterImg.append(pygame.image.load("monster.png"))
    monster_coordX.append(random.randint(0, 736))
    monster_coordY.append(random.randint(50, 150))
    monster_coordX_dx.append(3.5)
    monster_coordY_dy.append(40)
    random_directions.append(random.choice(tuple))


def monster(x, y, i):
    screen.blit(monsterImg[i], (x, y))


# Bullet
bulletImg = pygame.image.load("bullet.png")
bullet_coordY = 480
bullet_coordY_dy = 10  # speed of vertical movement
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bulletImg, (x + 16, y))  # We add 16 to x-axis, otherwise bullet would leave from spaceship's left side


# Background
backgroundImg = pygame.image.load("background.png")
background_coordX = 0
background_coordY = 0


def background(x, y):
    screen.blit(backgroundImg, (x, y))


# Score
score_value = 0
score_font = pygame.font.Font("Minecrafter.Reg.ttf", 30)


def show_score(x, y):
    score_text = score_font.render(f"SCORE: {score_value}", True, (255, 255, 255))
    screen.blit(score_text, (x, y))


# Background sound
mixer.music.load("naruto_theme.mp3")
mixer.music.play(-1)

# Game Over
game_over_state = False
game_over_font = pygame.font.Font("Transformers.ttf", 64)
play_again_font = pygame.font.Font("Transformers.ttf", 34)
Yes_or_No_font = pygame.font.Font("nasa.ttf", 34)


def show_game_over():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    play_again_text = play_again_font.render("Play again?", True, (255, 255, 255))
    Yes_or_No_text = Yes_or_No_font.render("[Y]   [N]", True, (255, 255, 255))
    screen.blit(game_over_text, (250, 250))
    screen.blit(play_again_text, (310, 320))
    screen.blit(Yes_or_No_text, (340, 370))


# MAIN GAME LOOP
running = True

while running:
    # RGB (Red, Green, Blue) and background
    screen.fill((0, 0, 0))
    background(background_coordX, background_coordY)

    # Calling the player function to make him appear
    player(player_coordX, player_coordY)

    for event in pygame.event.get():
        # Quit the game
        if event.type == pygame.QUIT:
            running = False
        # Bullet appearance (from "ready" to "fired")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if bullet_state == "ready":
                    mixer.Sound("kunaithrow.wav").play()
                    # Get the current X coordinate of spaceship
                    bullet_coordX = player_coordX
                    fire_bullet(bullet_coordX, bullet_coordY)
            if event.key == pygame.K_y:
                for i in range(n_monsters):
                    score_value = 0
                    monster_coordY[i] = random.randint(50, 150)
            if event.key == pygame.K_n:
                running = False

    # Bullet movement
    if bullet_coordY <= -10:
        bullet_coordY = 480
        bullet_state = "ready"
    if bullet_state == "fired":
        fire_bullet(bullet_coordX, bullet_coordY)
        bullet_coordY -= bullet_coordY_dy

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_coordX -= player_coordX_dx
    if keys[pygame.K_RIGHT]:
        player_coordX += player_coordX_dx

    # Monsters' movement, collision, border checking and GAME OVER

    for i in range(n_monsters):
        # Calling the monster function to make them appear
        monster(monster_coordX[i], monster_coordY[i],i)
        # Movement
        monster_coordX[i] += monster_coordX_dx[i] * random_directions[i]
        # Collision with bullet
        if bullet_coordY - 16 <= monster_coordY[i] + 32 and \
                bullet_coordY - 16 >= monster_coordY[i] - 32 and \
                bullet_coordX >= monster_coordX[i] - 32 and \
                bullet_coordX <= monster_coordX[i] + 32:
            mixer.Sound("kunaihit.wav").play()
            bullet_coordY = 480
            bullet_state = "ready"
            score_value += 1
            monster_coordX[i] = random.randint(0, 736)
            monster_coordY[i] = random.randint(50, 150)
        # Border checking
        if monster_coordX[i] < 0:
            monster_coordX_dx[i] *= -1
            monster_coordY[i] += monster_coordY_dy[i]
        if monster_coordX[i] > 736:
            monster_coordX_dx[i] *= -1
            monster_coordY[i] += monster_coordY_dy[i]

        # Game Over
        if monster_coordY[i] > 420:
            show_game_over()
            for i in range(n_monsters):
                monster_coordY[i] = 660

    # Checking borders of Player
    if player_coordX < 0:
        player_coordX = 0
    if player_coordX > 736:
        player_coordX = 736

    show_score(10, 10)
    pygame.display.update()
