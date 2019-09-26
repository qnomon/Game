import pygame
import random

pygame.init()

black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]
orange = [255, 102, 0]
yellow = [255, 255, 0]
green = [0, 255, 0]
blue = [0, 0, 255]
purple = [128, 0, 128]

FPS = 15
clock = pygame.time.Clock()

block_s = 30
screen_w, screen_h = 900, 600
assert screen_w % block_s == 0, 'Window width must be multiple of tile side.'
assert screen_h % block_s == 0, 'Window height must be multiple of tile side.'
screen = pygame.display.set_mode((screen_w, screen_h), 0, 32)
pygame.display.set_caption('Communism Simulator 2')



font = pygame.font.SysFont(None, 24)

def playMusic(path):
    song = pygame.mixer.Sound(random.choice(path))
    song.play()

def message(msg, color, x, y):
    text = font.render(msg, True, color)
    screen.blit(text, [x, y])

def loadSprite(path, x, y):
    return pygame.transform.scale((pygame.image.load(path).convert_alpha()),(x,y))

gameover = loadSprite('images/gameover.png', screen_w, screen_h)
background = loadSprite('images/background.png', screen_w, screen_h)
menu = loadSprite('images/menu.png', screen_w, screen_h)

item = loadSprite('images/item.png', block_s, block_s)
vodka = loadSprite('images/powerup.png', block_s, block_s)
wall = loadSprite('images/wall.png', block_s, block_s)

leadup = loadSprite('images/leadup.png', block_s, block_s)
leaddown = loadSprite('images/leaddown.png', block_s, block_s)
leadright = loadSprite('images/leadright.png', block_s, block_s)
leadleft = loadSprite('images/leadleft.png', block_s, block_s)

enemyup = loadSprite('images/enemyup.png', block_s, block_s)
enemydown = loadSprite('images/enemydown.png', block_s, block_s)
enemyright = loadSprite('images/enemyright.png', block_s, block_s)
enemyleft = loadSprite('images/enemyleft.png', block_s, block_s)

bulletup = loadSprite('images/bulletup.png', block_s, block_s)
bulletdown = loadSprite('images/bulletdown.png', block_s, block_s)
bulletright = loadSprite('images/bulletright.png', block_s, block_s)
bulletleft = loadSprite('images/bulletleft.png', block_s, block_s)


def loadMap(path):
    wall_coords = []
    enemy_coords = []
    file = open(path, 'r')
    file = str(file.read())
    file = file.split('\n')
    for row in range(len(file)):
        for column in range(len(file[row])):
            if file[row][column] == '@':
                lead_coords = [column*block_s, row*block_s]
            if file[row][column] == '#':
                wall_coords.append([column*block_s, row*block_s])
            if file[row][column] == 'e':
                enemy_coords.append([column*block_s, row*block_s])
    return [lead_coords, wall_coords, enemy_coords]


def mainLoop():
    lead_dir = leadup
    enemy_dir = enemyup
    lead_x_change = 0
    lead_y_change = 0
    lead_coords, wall_coords, enemy_coords = loadMap('map.txt')
    lead_x, lead_y = lead_coords

    bullet_coords = []
    bullet_dir = bulletup
    bulletMotion = False

    gameOver = False
    while True:
        while gameOver == True:
            screen.blit(gameover, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        pygame.quit()
                        quit()
                    elif event.key == pygame.K_y:
                        mainLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_dir = leadleft
                    lead_x_change = -block_s
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_dir = leadright
                    lead_x_change = block_s
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_dir = leadup
                    lead_y_change = -block_s
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_dir = leaddown
                    lead_y_change = block_s
                    lead_x_change = 0

                if event.key == pygame.K_z and bulletMotion == False:
                    if lead_dir == leadup:
                        bullet_coords.append(lead_x)
                        bullet_coords.append(lead_y)
                        bullet_dir = bulletup

                    elif lead_dir == leaddown:
                        bullet_coords.append(lead_x)
                        bullet_coords.append(lead_y)
                        bullet_dir = bulletdown

                    if lead_dir == leadright:
                        bullet_coords.append(lead_x)
                        bullet_coords.append(lead_y)
                        bullet_dir = bulletright

                    if lead_dir == leadleft:
                        bullet_coords.append(lead_x)
                        bullet_coords.append(lead_y)
                        bullet_dir = bulletleft
                    bulletMotion = True


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    lead_x_change = 0
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = 0
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_x_change = 0
                    lead_y_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_x_change = 0
                    lead_y_change = 0

        if bulletMotion == True:
            if bullet_dir == bulletup:
                bullet_coords[1] -= block_s
            elif bullet_dir == bulletdown:
                bullet_coords[1] += block_s
            elif bullet_dir == bulletright:
                bullet_coords[0] += block_s
            elif bullet_dir == bulletleft:
                bullet_coords[0] -= block_s

            if bullet_coords in wall_coords:
                bullet_coords = []
                bulletMotion = False
            elif bullet_coords in enemy_coords:
                enemy_coords.remove(bullet_coords)

        if [lead_x + lead_x_change, lead_y + lead_y_change] in wall_coords:
            lead_x_change = 0
            lead_y_change = 0


        for coordinate in enemy_coords:
            direction = random.choice(['X', 'Y'])
            if direction == 'X':
                if coordinate[0] > lead_x:
                    if [coordinate[0] - block_s, coordinate[1]] in wall_coords:
                        continue
                    else:
                        enemy_dir = enemyleft
                        coordinate[0] -= block_s

                elif coordinate[0] < lead_x:
                    if [coordinate[0] + block_s, coordinate[1]] in wall_coords:
                        continue
                    else:
                        enemy_dir = enemyright
                        coordinate[0] += block_s

            elif direction == 'Y':
                if coordinate[1] > lead_y:
                    if [coordinate[0], coordinate[1] - block_s] in wall_coords:
                        continue
                    else:
                        enemy_dir = enemyup
                        coordinate[1] -= block_s

                elif coordinate[1] < lead_y:
                    if [coordinate[0], coordinate[1] + block_s] in wall_coords:
                        continue
                    else:
                        enemy_dir = enemydown
                        coordinate[1] += block_s

        if [lead_x, lead_y] in enemy_coords:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        screen.blit(background, (0, 0))
        screen.blit(lead_dir, (lead_x, lead_y))
        for i in wall_coords:
            screen.blit(wall, (i[0], i[1]))
        for i in enemy_coords:
            screen.blit(enemy_dir, (i[0], i[1]))
        if bulletMotion == True:
            screen.blit(bullet_dir, (bullet_coords[0], bullet_coords[1]))

        pygame.display.update()
        clock.tick(FPS)
mainLoop()