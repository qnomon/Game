# !/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random

WHITE = (255, 255, 255)
RED = (192, 0, 0)
GREEN = (0, 192, 0)
BLUE = (0, 0, 192)
YELLOW = (238, 201, 0)


class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 708))
        self.bird = pygame.Rect(65, 50, 45, 30)
        self.background = pygame.image.load("assets/background.png").convert()
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)

    def updateWalls(self):
        self.wallx -= 3
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2
        self.bird[1] = self.birdY
        upRect = pygame.Rect(self.wallx,  # Rect(left, top, width, height)
                             360 + self.gap - self.offset,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height() + 10)
        middleRect = pygame.Rect(self.wallx + 150, 230 + self.gap - self.offset, 1, self.gap)  # Vertical
        divisionRect = pygame.Rect(0, 320 + self.gap - self.offset, 400, 1)  # Horizontal
        divisionRect2 = pygame.Rect(0, 360 + self.gap - self.offset, 400, 1)
        divisionRect3 = pygame.Rect(0, 400 + self.gap - self.offset, 400, 1)

        # pygame.draw.rect(self.screen, RED, upRect, 3)
        # pygame.draw.rect(self.screen, RED, downRect, 3)

        # pygame.draw.rect(self.screen, BLUE, middleRect, 3)
        # pygame.draw.rect(self.screen, YELLOW, divisionRect, 3)
        # pygame.draw.rect(self.screen, YELLOW, divisionRect2, 3)
        # pygame.draw.rect(self.screen, YELLOW, divisionRect3, 3)

        if upRect.colliderect(self.bird):
            self.dead = True
        if downRect.colliderect(self.bird):
            self.dead = True

        # AI
        if divisionRect.colliderect(self.bird) or divisionRect2.colliderect(self.bird) or divisionRect3.colliderect(
                self.bird) or middleRect.colliderect(self.bird) and self.dead == False:
            self.jump = 17  # Simula um clique
            self.gravity = 5
            self.jumpSpeed = 10

        if not 0 < self.bird[1] < 720:
            self.bird[1] = 50
            self.birdY = 50
            self.dead = False
            self.counter = 0
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.Font('assets/Flappy Bird Font.ttf', 50)
        font2 = pygame.font.Font('assets/Flappy Bird Font.ttf', 55)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font2.render(str(self.counter), -1, (0, 0, 0)), (200, 50))
            self.screen.blit(font.render(str(self.counter), -1, (255, 255, 255)), (200, 50))

            # View collision rectangles
            # pygame.draw.rect(self.screen, RED, self.bird, 3)

            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1
            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))
            if not self.dead:
                self.sprite = 0
            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()


if __name__ == "__main__":
    FlappyBird().run()
flappybird.py
Displaying
flappybird.py