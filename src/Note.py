from Variables import *
from Colors import *

class Note:

    def __init__(self, color, start, beat, speed, surface, screenSize):
        #creates a note object which will move across the screen.
        self.color = color
        self.start = start
        self.beat = beat
        self.speed = speed
        self.surf = surface
        if start == -1:
            self.posX = (screenSize[0] / 2) + (screenSize[0] * 0.89)
        elif start == 1:
            self.posX = (screenSize[0] / 2) - (screenSize[0] * 0.925)
        self.rect = pygame.Rect(self.posX, (screenSize[1] * 0.75) - (screenSize[1] * 0.025), screenSize[1] * 0.05, screenSize[1] * 0.05)
        self.active = True

    def move(self, zone):
        #moves the note object a certain amount and then redraws it
        moveAmt = self.speed * self.start
        self.rect = pygame.Rect.move(self.rect, moveAmt, 0)
        pygame.draw.ellipse(self.surf, self.color, self.rect)
        if self.rect.colliderect(zone):
            self.delete()
            return "del"

    def delete(self):
        #deletes the note
        self.active = False
