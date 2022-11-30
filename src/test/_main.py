import pygame, time, sys, math
from pygame import mixer
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


def UpdateScore(amount, score):
    grade = ""
    if amount == 100:
        grade = "Perfect"
    elif amount == 80:
        grade = "Great"
    elif amount == 50:
        grade = "OK"
    elif amount == 0:
        grade = "Miss"
    print(f"{grade}: {amount}")
    newScore = [score[0], score[1], score[2]]
    newScore[1] += amount
    newScore[2] += 100
    newScore[0] = round((newScore[1] / newScore[2]) * 100, 1)
    return newScore


def progressSequence(num, song, score):
    for note in notes:
        if note.active:
            note.move(dt, delZone)
        else:
            notes.remove(note)
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
def music():
    mixer.music.load('Upbeat_Tutorial_Final.mp3')
    mixer.music.set_volume(0.2)
    mixer.music.play()

# Setup ------------------------------------------------------- #
record = Record(screenSize, game_surf)
blueBtn = Button("W", blue, record, screenSize)
orangeBtn = Button("E", orange, record, screenSize)
greenBtn = Button("S", green, record, screenSize)
magentaBtn = Button("N", magenta, record, screenSize)

notes = []
currentNote = 0
delZone = pygame.Rect(screenSize[0] / 2, screenSize[1] / 2, 10, 500)

score = [0, 0, 0]
# actual score percentage, raw score value, total potential score value

music()

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
        currentNote = progressSequence(currentNote, s1, score)

    # update beat count
    beat = UpdateBeat(beat)
    beatTotal += UpdateBeat(beatTotal, True)

    # score
    sc = font2.render(f"{score[0]}", False, "white")
    sc_rect = sc.get_rect(center=(screenSize[0] / 10, screenSize[1] / 10))
    txt_surf.blit(sc, sc_rect)
    # Input ------------------------------------------------ #
    for event in pygame.event.get():
        amnt = 0
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
                        amnt = btn.pressed(notes)
                        if amnt >= 0:
                            score = UpdateScore(amnt, score)
            if event.key == pygame.K_d:
                for btn in record.buttons:
                    if btn.orientation == "E":
                        amnt = btn.pressed(notes)
                        if amnt >= 0:
                            score = UpdateScore(amnt, score)
            if event.key == pygame.K_SPACE:
                record.spin()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                for btn in record.buttons:
                    if btn.orientation == "W":
                        btn.pressed(notes, "!")
            if event.key == pygame.K_d:
                for btn in record.buttons:
                    if btn.orientation == "E":
                        btn.pressed(notes, "!")

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
