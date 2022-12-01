import pygame, time, sys, math
from pygame import mixer
from Variables import *
from Colors import *
from Record import Record
from Button import Button
from Note import Note
from Sequences import s1

mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('UpBeat')


# Functions ------------------------------------------------------- #

def UpdateBeat(b, total=False):
    beatsPerFrame = (bpm / 60) / framerate
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
    print(score[0])
    return newScore

def progressSequence(num, song):
    for note in notes:
        if note.active:
            if note.move(delZone) == "del":
                global score
                score = UpdateScore(0, score)
        else:
            notes.remove(note)
    notesToSpawn = []
 
    for note in song:
        if song.index(note) > num:
            sHave = (((screenSize[0]) * (190/240))/noteSpeed)/framerate
            sNeed = (((note[2])-beatTotal)/bpm)*60
            if sNeed <= sHave:
                notesToSpawn.append(Note(note[0], note[1], note[2], noteSpeed, game_surf, screenSize))
                c = song.index(note)
    if len(notesToSpawn) == 0:
        return num
    for note in notesToSpawn:
        notes.append(note)
    return c

def music():
    sound1 = mixer.Sound("../assets\\Upbeat_Tutorial_Final.mp3")
    channel1 = mixer.Channel(0)
    mixer.music.set_volume(0.2)
    channel1.play(sound1)

#setup
screen.fill(bkg)
game_surf.fill(clear)
fx_surf.fill(clear)
font1 = pygame.font.Font(None, int(100))
font2 = pygame.font.Font(None, int(50))
font3 = pygame.font.SysFont("impact", int(screenSize[0]/7.5))

record = Record(screenSize, game_surf)
blueBtn = Button("W", blueBtn, record, screenSize)
orangeBtn = Button("E", orangeBtn, record, screenSize)
greenBtn = Button("S", greenBtn, record, screenSize)
magentaBtn = Button("N", magentaBtn, record, screenSize)
notes = [] #array of all active notes
currentNote = 0 #index number of the most recently spawned note
delZone = pygame.Rect(screenSize[0] / 2, screenSize[1] / 2, 10, 500) #zone where notes get deleted
score = [0, 0, 0]  # actual score percentage, raw score value, total potential score value
    #images
tableImg = pygame.image.load('../assets\\UpBeat_Table.png')
tableImg = pygame.transform.scale(tableImg, (screenSize[0], screenSize[0]))
djImg = pygame.image.load('../assets\\UpBeat_DJ.png')

#start
music()
last_time = time.time()

while True:
    dt = time.time() - last_time
    # VISUALS ------------------------------------------------------------------------------ #
        # surfaces
    screen.fill(bkg)
    game_surf.fill(pygame.Color(255, 255, 255, 0))
    fx_surf.fill(pygame.Color(255, 255, 255, 0))
    txt_surf.fill(pygame.Color(255, 255, 255, 0))

        # sprites
    if abs((beat*4) - round(beat*4)) < 0.1:
        djImg = pygame.transform.scale(djImg,
                                    (screenSize[1], screenSize[1] * 0.97))
        game_surf.blit(djImg, (0.2 * screenSize[0], -0.17 * screenSize[1]))
    else:
        djImg = pygame.transform.scale(djImg, (screenSize[1], screenSize[1]))
        game_surf.blit(djImg, (0.2 * screenSize[0], -0.2 * screenSize[1]))

    game_surf.blit(tableImg, (0, -0.57 * screenSize[1]))

        # draw the records and buttons
    record.draw(gray)

        # score
    sc = font3.render(f"{score[0]}%", False, lightBkg)
    sc_rect = sc.get_rect(center=(screenSize[0] / 6, screenSize[1] / 10))
    txt_surf.blit(sc, sc_rect)

    # GAME LOGIC ----------------------------------------------------------------------------- #
        # spawning notes
    if currentNote < len(s1):
        currentNote = progressSequence(currentNote, s1)

        # update beat count
    beat = UpdateBeat(beat)
    beatTotal += UpdateBeat(beatTotal, True)

    # INPUT ---------------------------------------------------------------------------------- #
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
                scratchSound = mixer.Sound('../assets\\Upbeat_Scratch.mp3')
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
    last_time = time.time()
    mainClock.tick(framerate)
    