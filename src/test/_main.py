import pygame, time, sys, math
from var import *
from colors import *
from Record import Record
from Button import Button
from Note import Note
from sequences import s1
# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption('UpBeat')

# World Vars ------------------------------------------------------- #

screen.fill(bkg)
game_surf.fill(clear)
fx_surf.fill(clear)

# Functions ------------------------------------------------------- #


def UpdateBeat(b, total=False):
    beatsPerFrame = (bpm / 60) / framerate
    b += beatsPerFrame
    if total == True:
        bct = font2.render(f"{round(b,1)}", False, "white")
        bct_rect = bct.get_rect(center=(screenSize[0] / 2, screenSize[1] / 4))
        txt_surf.blit(bct, bct_rect)
        return beatsPerFrame
    mn = font1.render("." * math.floor(b), False, "white")
    mn_rect = mn.get_rect(center=(screenSize[0] / 2, screenSize[1] / 2))
    bc = font2.render(f"{round(b,1)}", False, "white")
    bc_rect = bc.get_rect(center=(screenSize[0] / 2, screenSize[1] / 3))
    txt_surf.blit(bc, bc_rect)
    txt_surf.blit(mn, mn_rect)
    if b >= 9:
        b = 0
    return b


def progressSequence(num, song):
    for note in notes:
        note.move(dt)
    for note in song:
        if song.index(note) > num:
            c = song.index(note)
            if (noteSpeed / (screenSize[0] / 2)) >= ((note[2] - beatTotal) /
                                                     ((bpm / 60) / framerate)):
                notes.append(
                    Note(note[0], note[1], note[2], noteSpeed, game_surf,
                         screenSize))
                return c
    return num


# Setup ------------------------------------------------------- #
record = Record(screenSize, game_surf)
blueBtn = Button("W", blue, record, screenSize)
orangeBtn = Button("E", orange, record, screenSize)
greenBtn = Button("S", green, record, screenSize)
magentaBtn = Button("N", magenta, record, screenSize)

notes = []
currentNote = 0
# note = Note(green, -1, 5, 2, game_surf, screenSize)

# Loop ------------------------------------------------------- #
while True:

    dt = time.time() - last_time
    dt *= 60
    last_time = time.time()

    # Visuals --------------------------------------------- #

    # surfaces
    screen.fill(bkg)
    game_surf.fill(pygame.Color(255, 255, 255, 0))
    fx_surf.fill(pygame.Color(255, 255, 255, 0))
    txt_surf.fill(pygame.Color(255, 255, 255, 0))

    # draw the records and buttons
    record.draw(gray)

    # spawning notes
    if currentNote < len(s1):
        currentNote = progressSequence(currentNote, s1)

    # update beat count
    beat = UpdateBeat(beat)
    beatTotal += UpdateBeat(beatTotal, True)
    # Input ------------------------------------------------ #
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
    screen.blit(txt_surf, (0, 0))
    pygame.display.update()
    mainClock.tick(framerate)

# running = True
# while running:
#     for n in range(1, 9):
#         mn = font1.render("." * n, False, "white")
#         mn_rect = mn.get_rect(center=(screenSize[0] / 2, screenSize[1] / 2))
#         bc = font2.render(f"{beat}", False, "white")
#         bc_rect = bc.get_rect(center=(screenSize[0] / 2, screenSize[1] / 3))
#         game_surf.blit(mn, mn_rect)
#         game_surf.blit(bc, bc_rect)
#         pygame.display.flip()
#         pygame.time.wait(500)
#         beat += 0.125
