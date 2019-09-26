import pygame
from pygame.locals import *
import sys
import os

def events():
    for event in pygame.event.get():
        if event == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


#Superficies
W, H = 800, 600
HW , HH = W /2, H / 2
AREA = W * H
os.environ['SDL_VIDEO_WINDOW_POS'] = "50,50"

pygame.init()
CLOCK = pygame.time.Clock()
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("Teste de BG")
FPS = 120

bkgd = pygame.image.load('sky.png').convert()
x = 0

while True:
    events()
    rel_x = x % bkgd.get_rect().width

    DS.blit(bkgd  , (rel_x - bkgd.get_rect().width , 0))
    if rel_x < W:
        DS.blit(bkgd, (rel_x, 0))
    x -= 1
    pygame.display.update()
    CLOCK.tick(FPS)
