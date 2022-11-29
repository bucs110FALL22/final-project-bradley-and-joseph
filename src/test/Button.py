import pygame
from var import *
from colors import *


class Button:

    def __init__(self, ornt, col, record, screenSize):
        #creates a button in the desired position, with a designated,
        record.buttons.append(self)

        self.orientation = ornt
        self.color = col
        self.pos = [0, 0]
        self.on = False
        self.active = False
        self.screenS = screenSize

        if self.orientation == "E" or self.orientation == "W":
            xOffset = 70
            self.pos[1] = screenSize[1] * 0.75
            self.on = True
            if self.orientation == "E":
                self.pos[0] = (screenSize[0] / 2) + xOffset
            if self.orientation == "W":
                self.pos[0] = (screenSize[0] / 2) - xOffset
        if self.orientation == "N" or self.orientation == "S":
            yOffset = 25
            self.pos[0] = screenSize[0] / 2
            self.on = True
            if self.orientation == "S":
                self.pos[1] = (screenSize[1] * 0.75) + yOffset
            if self.orientation == "N":
                self.pos[1] = (screenSize[1] * 0.75) - yOffset

        btnWidth = 40
        btnHeight = 20
        self.rect = pygame.Rect(self.pos[0], self.pos[1], btnWidth, btnHeight)
        self.rect = pygame.Rect.move(self.rect, (btnWidth / 2) * -1,
                                     (btnHeight / 2) * -1)
        self.draw()

    def pressed(self, listOfNotes, param=None):
        # called when the button is pressed, changes the active variable
        self.active = False
        if param != "!":
            self.active = True
            for note in listOfNotes:
                if note.color == self.color:
                    if note.rect.colliderect(
                            pygame.Rect.inflate(self.rect, 40, 40)):
                        if note.rect.colliderect(self.rect):
                            if pygame.Rect.inflate(self.rect, 20,
                                                   20).contains(note.rect):
                                note.delete()
                                return 100
                            note.delete()
                            return 80
                        note.delete()
                        return 50
                else:
                    note.delete()
                    return 0
            return -1
        else:
            return -1

    def rotate(self, record):
        # When the record is rotated, this will change the orientation of the button
        newOrnt = ""
        if self.orientation == "N":
            newOrnt = "W"
        elif self.orientation == "E":
            newOrnt = "N"
        elif self.orientation == "S":
            newOrnt = "E"
        elif self.orientation == "W":
            newOrnt = "S"
        print(f"{self.orientation} becomes {newOrnt}")
        Button(newOrnt, self.color, record, self.screenS)

    def draw(self, glowColor=pygame.Color(255, 255, 255, 50)):
        # used to draw the buttons
        pygame.draw.ellipse(game_surf, self.color, self.rect)
        if self.active:
            glowRect = pygame.Rect.inflate(self.rect, 40, 20)
            pygame.draw.ellipse(fx_surf, glowColor, glowRect)
