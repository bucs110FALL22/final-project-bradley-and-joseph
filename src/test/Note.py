import pygame
from var import *
from colors import *


class Note:

    def __init__(self, color, start, beat, speed, surface, screenSize):
        self.color = color
        self.start = start
        self.beat = beat
        self.speed = speed
        self.surf = surface
        self.posX = (screenSize[0] / 2) + ((screenSize[0] * 0.9) * start * -1)
        self.rect = pygame.Rect(self.posX, (screenSize[1] * 0.75) - 40, 50, 50)

    def move(self, dTime):
        self.rect = pygame.Rect.move(self.rect,
                                     self.speed * self.start * dTime, 0)
        pygame.draw.ellipse(self.surf, self.color, self.rect)
        if self.posX < 0 or self.posX > screenSize[0]:
            del self

    def __del__(self):
        pass
