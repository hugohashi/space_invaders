#!/usr/bin/env python3

#imports
import pygame
import random
import math

#initializing pygame
pygame.init()

#create game screen
screen = pygame.display.set_mode((800, 600))

#background
background = pygame.image.load ('space.jpg')

#title
pygame.display.set_caption("Space Invaders")

#icon
icon = pygame.image.load ('ufo.png')
pygame.display.set_icon (icon)

#player
playerimg = pygame.image.load ('spaceship.png')
playerX = 380
playerY = 500
playerX_change = 0
playerY_change = 0

#enemies
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
n_of_enemy = 6

for i in range (n_of_enemy):
    enemyimg.append(pygame.image.load ('ghost.png'))
    enemyX.append(random.randint (0, 735))
    enemyY.append(random.randint(0, 200))
    enemyX_change.append(0.3)
    enemyY_change.append(35)

#bullet
# Ready: You can't see the bullet on the screen
# Fire: The bullet is currently moving
bulletimg = pygame.image.load ('bullet.png')
bulletX = 0
bulletY = playerY
bulletX_change = 0
bulletY_change = 1
bullet_state = 'ready'

#score
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 40)
textX = 10
textY = 10

#game over
game_over_font = pygame.font.Font('freesansbold.ttf', 80)

def player(x,y):
    screen.blit(playerimg, (x, y))

def enemy(x,y,i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x + 16, y + 10))

def is_collision(enemyX, enemyY, bulletX, bulletY):
   distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
   if distance < 27:
    return True

def show_score(x,y):
    score = score_font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = game_over_font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(over_text,(175,250))

#game loop
running = True
while running:

    #color the screen
    screen.fill((255, 255, 255))

    #background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:

            #player movement
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = +0.5

            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        #not pressing any keys anymore
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #Screen boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0

    if playerX >= 736:
       playerX = 736

    #enemy movement
    for i in range (n_of_enemy):
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]

        if enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        #Game over
        if enemyY[i] > 400:
            for j in range (n_of_enemy):
                enemyY[j] = 2000

            game_over_text()
            break

        #Collision
        collision = is_collision (enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = playerY
            bullet_state = 'ready'
            score_value += 10
        
            enemyX[i] = random.randint (0, 735)
            enemyY[i]  = random.randint(0, 200)
        
        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    if bulletY <= 0:
        bulletY = playerY
        bullet_state ='ready'

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
