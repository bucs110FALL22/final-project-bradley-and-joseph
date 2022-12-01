from Variables import *
from Colors import *


class Record:

    def __init__(self, screenSize, surface):
        #Creates the record in which the buttons will be drawn on
        self.surface = surface
        self.width = screenSize[0] / 3
        self.height = screenSize[1] / 4
        self.rect = pygame.Rect((screenSize[0] / 2) - (self.width / 2),
                                screenSize[1] * 0.75, self.width, self.height)
        self.rect = pygame.Rect.move(self.rect, 0, (self.height / 2) * -1)
        self.buttons = []

    def spin(self):
        #Spins the record and then tells the buttons to change position
        print("~~~~~~~~~~~~ Rotating Record ~~~~~~~~~~~~~~~")
        listOfBtns = self.buttons.copy()
        self.buttons.clear()
        # print(listOfBtns)
        for n in range(4):
            # print(n)
            btn = listOfBtns[n]
            print(f"rotating {btn.color}")
            btn.rotate(self)
        print("~~~~~~~~~~~~~~ Done Rotating ~~~~~~~~~~~~~~~~")

    def draw(self, color):
        #Draws the Record and then tells the buttons to draw themselves
        pygame.draw.ellipse(self.surface, color, self.rect)
        for btn in self.buttons:
            btn.draw()
