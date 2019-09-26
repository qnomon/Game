# importação das bibliotecas
import pygame
import random
from pygame.locals import *
pygame.init()
pygame.font.init()

score_value = 0
font = pygame.font.Font('freesansbold.ttf',24)
textX = 10
textY = 10


def show_score(x,y):
    score = font.render("Score: "+str(score_value),True,(255,255,255))
    screen.blit(score, (x,y))

def on_grid_random():  # função de randomizar a maçã no grid
    x = random.randint(0, 590)
    y = random.randint(0, 590)
    return (x // 10 * 10, y // 10 * 10)


def collision(c1, c2):  # colisão pra comer a maçã
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


def point():
    effect = pygame.mixer.Sound('point.wav')
    effect.play()



WHITE = (255, 255, 255)
font_name = pygame.font.match_font('arial')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# Configuração das direções em sentido horário
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
UP_ON = False
DOWN_ON = False
LEFT_ON = True
RIGHT_ON = False


screen = pygame.display.set_mode((600, 600))  # criação da janela
pygame.display.set_caption('Snake')  # titulo da janela

# propriedades da cobra
snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((95, 176, 14))

# propriedades da maça
apple = pygame.Surface((10, 10))
apple.fill((173, 7, 7))
apple_pos = on_grid_random()

my_direction = LEFT  # direção inicial
clock = pygame.time.Clock()  # limitador de fps


while True:  # laço infinito do jogo
    clock.tick(20)  # limitador implementado
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            # eventos que definem a mudança de direção
        if event.type == KEYDOWN:
            if event.key == K_UP and not DOWN_ON:
                my_direction = UP
                UP_ON = True
                LEFT_ON = False
                RIGHT_ON = False
                DOWN_ON = False
            if event.key == K_DOWN and not UP_ON:
                my_direction = DOWN
                UP_ON = False
                LEFT_ON = False
                RIGHT_ON = False
                DOWN_ON = True
            if event.key == K_LEFT and not RIGHT_ON:
                my_direction = LEFT
                UP_ON = False
                LEFT_ON = True
                RIGHT_ON = False
                DOWN_ON = False
            if event.key == K_RIGHT and not LEFT_ON:
                my_direction = RIGHT
                UP_ON = False
                LEFT_ON = False
                RIGHT_ON = True
                DOWN_ON = False
    # Quando a cobra come a maçã
    if collision(snake[0], apple_pos):
        point()
        apple_pos = on_grid_random()
        snake.append((0, 0))
        score_value += 10

    # colisão com ela mesma
    if snake[0] in snake[1:]:
        break

    # colisão com a parede
    if snake[0][0] == 0 or snake[0][0] == 600:
        break
    if snake[0][1] == 0 or snake[0][1] == 600:
        break

    # como a cobra se movimenta
    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i - 1][0], snake[i - 1][1])

    # direções da cobra
    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])

    screen.fill((9, 28, 0))  # atualizando a tela com preto
    screen.blit(apple, apple_pos)  # traçando a maça

    for pos in snake:
        screen.blit(snake_skin, pos)
    show_score(textX,textY)
    pygame.display.update()
pygame.quit()
