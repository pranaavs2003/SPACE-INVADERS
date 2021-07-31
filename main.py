import pygame
import random
import math
from pygame import mixer

# Windiow Settings
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)
background = pygame.image.load("bg.jpg")

#background Music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_X = 10
test_Y = 10

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Player
player_img = pygame.image.load("player1.png")
player_X = 370
player_Y = 480
velocity_X = 0
velocity_Y = 0

# Enemy
enemy_img = []
enemy_Y = []
enemy_X = []
velocity_enemy_X = []
velocity_enemy_Y = []
n = 7
for i in range(n):
    enemy_img.append(pygame.image.load("enemy1.png"))
    enemy_Y.append(random.randint(50,200))
    enemy_X.append(random.randint(0,150))
    velocity_enemy_X.append(1)
    velocity_enemy_Y.append(0.08)


# Bullet
bullet_img = pygame.image.load("bullet.png")
bullet_X = 0
bullet_Y = 480
velocity_bullet_Y = 2
bullet_state = "ready"

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(player_X, player_Y):
    screen.blit(player_img, (player_X, player_Y))
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x+28, y+10))
def isCollision(enemy_X, enemy_Y, bullet_X, bullet_Y):
    distance = math.sqrt(math.pow(enemy_X - bullet_X, 2) + (math.pow(enemy_Y - bullet_Y, 2)))
    if distance < 45 and bullet_state=="fire":
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))
    show_score(text_X, test_Y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                velocity_X = -1
            if event.key == pygame.K_RIGHT:
                velocity_X = 1
            if event.key == pygame.K_UP:
                velocity_Y = -1
            if event.key == pygame.K_DOWN:
                velocity_Y = 1
            if event.key == pygame.K_SPACE:
                if bullet_state=="ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    # print("pew!")
                    bullet_X = player_X
                    bullet_Y = player_Y
                    fire_bullet(bullet_X,bullet_Y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                velocity_X = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                velocity_Y = 0

    player_X += velocity_X
    player_Y += velocity_Y
    if player_X <= 0:
        player_X = 0
    elif player_Y <= 0:
        player_Y = 0
    elif player_X >= 700:
        player_X = 700
    elif player_Y >= 500:
        player_Y = 500



    for i in range(n):
        if enemy_Y[i] > 420:
            for j in range(n):
                enemy_Y[j] = 2000
            game_over_text()
            break

        if enemy_X[i] >= 735:
            velocity_enemy_X[i] = -1
        if enemy_X[i] <= 0:
            velocity_enemy_X[i] = 1
        if enemy_X[i] >=780:
            enemy_X[i] = random.randint(50, 750)
            enemy_Y[i] = random.randint(0, 150)

        enemy_X[i] += velocity_enemy_X[i]
        enemy_Y[i] += velocity_enemy_Y[i]

        collision = isCollision(enemy_X[i],enemy_Y[i],bullet_X,bullet_Y)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bullet_Y = player_Y
            bullet_state = "ready"
            score_value+=1
            print(score_value)
            enemy_X[i] = random.randint(50, 750)
            enemy_Y[i] = random.randint(0, 150)
        enemy(enemy_X[i], enemy_Y[i],i)

    if bullet_Y<0 :
        bullet_Y=player_Y
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_X,bullet_Y)
        bullet_Y -= velocity_bullet_Y



    player(player_X, player_Y)

    pygame.display.update()
