from Variables import *
from Colors import *
import math


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

        btnWidth = record.width * 0.2
        btnHeight = btnWidth / 2
        self.wh = (btnWidth,btnHeight)

        if self.orientation == "E" or self.orientation == "W":
            xOffset = btnWidth * 1.75
            self.pos[1] = screenSize[1] * 0.75
            self.on = True
            if self.orientation == "E":
                self.pos[0] = (screenSize[0] / 2) + xOffset
            if self.orientation == "W":
                self.pos[0] = (screenSize[0] / 2) - xOffset
        if self.orientation == "N" or self.orientation == "S":
            yOffset = btnHeight * 1.5
            self.pos[0] = screenSize[0] / 2
            self.on = True
            if self.orientation == "S":
                self.pos[1] = (screenSize[1] * 0.75) + yOffset
            if self.orientation == "N":
                self.pos[1] = (screenSize[1] * 0.75) - yOffset

        
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
                if note.rect.colliderect(pygame.Rect.inflate(
                        self.rect, self.wh[0], self.wh[0])):
                    if self.color == blueBtn:
                        noteCol = blue
                    if self.color == orangeBtn:
                        noteCol = orange
                    if self.color == greenBtn:
                        noteCol = green
                    if self.color == magentaBtn:
                        noteCol = magenta
                    if note.color == noteCol:
                        if note.rect.colliderect(self.rect):
                            if pygame.Rect.inflate(self.rect, self.wh[1],
                                                   self.wh[1]).contains(note.rect):
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
        infNum = int(round(self.wh[1]))
        if self.orientation == "N":
            newOrnt = "W"
            pygame.draw.arc(game_surf, self.color,
                            pygame.Rect.inflate(record.rect, -1 * infNum , -1 * infNum),
                            math.pi * 0.75, math.pi, infNum//2)
        elif self.orientation == "E":
            newOrnt = "N"
            pygame.draw.arc(game_surf, self.color,
                            pygame.Rect.inflate(record.rect, -1 * infNum , -1 * infNum), math.pi * 0.25,
                            math.pi / 2, infNum//2)
        elif self.orientation == "S":
            newOrnt = "E"
            pygame.draw.arc(game_surf, self.color,
                            pygame.Rect.inflate(record.rect, -1 * infNum , -1 * infNum),
                            math.pi * 1.75, 2 * math.pi, infNum//2)
        elif self.orientation == "W":
            newOrnt = "S"
            pygame.draw.arc(game_surf, self.color,
                            pygame.Rect.inflate(record.rect, -1 * infNum , -1 * infNum),
                            math.pi * 1.25, math.pi * 1.5, infNum//2)
        print(f"{self.orientation} becomes {newOrnt}")
        Button(newOrnt, self.color, record, self.screenS)
        self.active = False
        self.draw()

    def draw(self, glowColor=pygame.Color(255, 255, 255, 50)):
        # used to draw the buttons
        pygame.draw.ellipse(game_surf, self.color, self.rect)
        if self.active:
            glowRect = pygame.Rect.inflate(self.rect, self.wh[0], self.wh[1])
            pygame.draw.ellipse(fx_surf, glowColor, glowRect)
