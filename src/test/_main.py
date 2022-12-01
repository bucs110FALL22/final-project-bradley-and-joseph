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
    beatsPerFrame = (bpm / 120) / framerate
    b += beatsPerFrame
    if total == True:
        # DEBUGGING TEXT
        # bct = font2.render(f"{round(b,1)}", False, "white")
        # bct_rect = bct.get_rect(center=(screenSize[0] / 2, screenSize[1] / 4))
        # txt_surf.blit(bct, bct_rect)
        return beatsPerFrame
    # DEBUGGING TEXT
    # mn = font1.render("." * math.floor(b / (1/8)), False, "white")
    # mn_rect = mn.get_rect(center=(screenSize[0] / 2, screenSize[1] / 2))
    # bc = font2.render(f"{round(b,1)}", False, "white")
    # bc_rect = bc.get_rect(center=(screenSize[0] / 2, screenSize[1] / 3))
    # txt_surf.blit(bc, bc_rect)
    # txt_surf.blit(mn, mn_rect)
    if b >= 1:
        b = b - 1
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


def progressSequence(num, song):
    for note in notes:
        if note.active:
            note.move(dt, delZone)
        else:
            notes.remove(note)
    notesToSpawn = []
    for note in song:
        if song.index(note) > num:
            if (noteSpeed / (screenSize[0] / 2)) >= ((note[2] - beatTotal) / ((bpm / 60) / framerate)):
                notesToSpawn.append(Note(note[0], note[1], note[2], noteSpeed, game_surf, screenSize))
                c = song.index(note)
    if len(notesToSpawn) == 0:
        return num
    for note in notesToSpawn:
        notes.append(note)
    return c


def music():
    sound1 = mixer.Sound("Upbeat_Tutorial_Final.mp3")
    channel1 = mixer.Channel(0)
    mixer.music.set_volume(0.2)
    channel1.play(sound1)


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

#images
tableImg = pygame.image.load('UpBeat_Table.png')
tableImg = pygame.transform.scale(tableImg, (screenSize[0], screenSize[0]))
djImg = pygame.image.load('UpBeat_DJ.png')

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

    # sprites
    if (beat - round(beat)) < 0.15:
        djImg = pygame.transform.scale(djImg,
                                       (screenSize[1], screenSize[1] * 0.97))
        game_surf.blit(djImg, (0.2 * screenSize[0], -0.15 * screenSize[1]))
    else:
        djImg = pygame.transform.scale(djImg, (screenSize[1], screenSize[1]))
        game_surf.blit(djImg, (0.2 * screenSize[0], -0.2 * screenSize[1]))

    game_surf.blit(tableImg, (0, -0.57 * screenSize[1]))

    # draw the records and buttons
    record.draw(gray)

    # spawning notes
    if currentNote < len(s1):
        currentNote = progressSequence(currentNote, s1)

    # update beat count
    beat = UpdateBeat(beat)
    beatTotal += UpdateBeat(beatTotal, True)

    # score
    sc = font2.render(f"{score[0]}%", False, "white")
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
                scratchSound = mixer.Sound('Upbeat_Scratch.mp3')
                channel2 = mixer.Channel(1)
                mixer.music.set_volume(0.4)
                channel2.play(scratchSound)
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
