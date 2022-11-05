import pygame, time, sys
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('UpBeat')


# Classes ------------------------------------------------------- #
class Record:

    def __init__(self):
        self.width = screenSize[0] / 3
        self.height = screenSize[1] / 4
        self.rect = pygame.Rect((screenSize[0] / 2) - (self.width / 2),
                                screenSize[1] * 0.75, self.width, self.height)
        self.rect = pygame.Rect.move(self.rect, 0, (self.height / 2) * -1)
        self.buttons = []
        self.draw()

    def spin(self):
        for btn in self.buttons:
            btn.rotate()

    def draw(self):
        pygame.draw.ellipse(game_surf, gray, self.rect)
        for btn in self.buttons:
            btn.draw()


class Button:

    def __init__(self, ornt, col, record):

        record.buttons.append(self)

        self.orientation = ornt
        self.color = col
        self.pos = [0, 0]
        self.on = False
        self.active = False

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

    def pressed(self, param=None):
        self.active = False
        if param != "!":
            self.active = True

    def rotate(self):
        newOrnt = ""
        if self.orientation == "N":
            newOrnt = "W"
        if self.orientation == "E":
            newOrnt = "N"
        if self.orientation == "S":
            newOrnt = "E"
        if self.orientation == "W":
            newOrnt = "S"

    def draw(self):
        pygame.draw.ellipse(game_surf, self.color, self.rect)
        if self.active:
            glowRect = pygame.Rect.inflate(self.rect, 40, 20)
            pygame.draw.ellipse(fx_surf, glow, glowRect)


##

# Functions ------------------------------------------------------- #

# World Vars ------------------------------------------------------- #
last_time = time.time()
framerate = 60
tempo = 60
beat = 0

screen = pygame.display.set_mode()
screenSize = pygame.display.get_window_size()

game_surf = pygame.Surface((screenSize[0], screenSize[1]), pygame.SRCALPHA)
fx_surf = pygame.Surface((screenSize[0], screenSize[1]), pygame.SRCALPHA)

font1 = pygame.font.Font(None, int(100))
font2 = pygame.font.Font(None, int(50))

bkg = pygame.Color(45, 30, 100)
gray = pygame.Color(55, 50, 60)
blue = pygame.Color(0, 200, 255)
orange = pygame.Color(255, 160, 0)
green = pygame.Color(0, 255, 0)
magenta = pygame.Color(255, 0, 255)
glow = pygame.Color(255, 255, 255, 50)
clear = pygame.Color(255, 255, 255, 0)

screen.fill(bkg)
game_surf.fill(clear)
fx_surf.fill(clear)

# Setup ------------------------------------------------------- #
record = Record()
blueBtn = Button("W", blue, record)
orangeBtn = Button("E", orange, record)
greenBtn = Button("S", green, record)
magentaBtn = Button("N", magenta, record)

# Loop ------------------------------------------------------- #
while True:

    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    # Visuals --------------------------------------------- #
    game_surf.fill(pygame.Color(255, 255, 255, 0))
    fx_surf.fill(pygame.Color(255, 255, 255, 0))
    record.draw()

    # r = pygame.Rect(pos, 200, 100, 100)
    # pygame.draw.rect(screen, (255, 255, 255), r)

    # Gameplay ------------------------------------------------ #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_a:
                for btn in record.buttons:
                    if btn.orientation == "W":
                        btn.pressed()
            if event.key == pygame.K_d:
                for btn in record.buttons:
                    if btn.orientation == "E":
                        btn.pressed()
            if event.key == pygame.K_SPACE:
                pass
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                for btn in record.buttons:
                    if btn.orientation == "W":
                        btn.pressed("!")
            if event.key == pygame.K_d:
                for btn in record.buttons:
                    if btn.orientation == "E":
                        btn.pressed("!")
    # Update ------------------------------------------------- #
    screen.blit(game_surf, (0, 0))
    screen.blit(fx_surf, (0, 0))
    pygame.display.update()
    mainClock.tick(framerate)

# while running:
#     for n in range(1, 9):
#         mn = font1.render("." * n, False, "white")
#         mn_rect = mn.get_rect(center=(screenSize[0] / 2, screenSize[1] / 2))
#         bc = font2.render(f"{beat}", False, "white")
#         bc_rect = bc.get_rect(center=(screenSize[0] / 2, screenSize[1] / 3))
#         screen.blit(mn, mn_rect)
#         screen.blit(bc, bc_rect)
#         pygame.display.flip()
#         pygame.time.wait(500)
#         beat += 0.125
