import pygame
import random
import math

# Initialize pygame
pygame.init()
pygame.mixer.init()
music = False

def soundtrack():
    global music
    if music == False:
        pygame.mixer.music.load('soundtrack.mp3')
        pygame.mixer.music.play(-1)
        music = True

def shoot():
    effect = pygame.mixer.Sound('shoot.wav')
    effect.play()

def point():
    effect = pygame.mixer.Sound('point.wav')
    effect.play()



# create the screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Space Fatecs")
icon = pygame.image.load('Spaceship.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('Spaceship.png')
playerX = 370
playerY = 520
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('Enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(0.15)
    enemyY_change.append(40)

# Bullet
# Ready = You can't see the bullet on the screen
# Fire = The bullet is currently moving
bulletImg = [pygame.image.load('shoot_1.png'), pygame.image.load('shoot_2.png'), pygame.image.load('shoot_3.png')]
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 0.1
bullet_state = "ready"
bullet_maxframe = 3
bullet_frame = 0


#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',24)
textX = 10
textY = 10


def show_score(x,y):
    score = font.render("Score: "+str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state, bullet_frame
    bullet_state = "fire"
    screen.blit(bulletImg[bullet_frame], (x + 26, y + 10))
    if bullet_frame > bullet_maxframe:
        bullet_frame = 0
    bullet_frame =+ 1

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # Standard background
    screen.fill((0, 0, 16))
    soundtrack()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Directional inputs
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_z:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Creating Bounds of spaceship
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement and bounds
    for i in range (num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.15
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.15
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 10
            point()
            enemyX[i] = random.randint(0, 735)
            enemyY[i]= random.randint(0, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX,textY)

    pygame.display.update()

