import pygame, time, sys, math
from pygame import mixer
from Variables import *
from Colors import *
from Record import Record
from Button import Button
from Note import Note
from Sequences import s1
from Sequences import s2

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
    global streak
    if amount == 100:
        grade = "Perfect"
        streak += 1
    elif amount == 80:
        grade = "Great"
    elif amount == 50:
        grade = "OK"
        streak = 0
    elif amount == 0:
        grade = "Miss"
        streak = 0
        missSound = mixer.Sound('../assets/UpBeat_Miss.mp3')
        channel3 = mixer.Channel(3)
        missSound.set_volume(0.4)
        channel3.play(missSound)
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
    magicNumber = 19/24
    for note in song:
        if song.index(note) > num:
            sHave = (((screenSize[0]) * magicNumber)/noteSpeed)/framerate
            sNeed = (((note[2])-beatTotal)/bpm)*60
            if sNeed <= sHave:
                notesToSpawn.append(Note(note[0], note[1], note[2], noteSpeed, game_surf, screenSize))
                c = song.index(note)
            else:
                break
    if len(notesToSpawn) == 0:
        return num
    for note in notesToSpawn:
        notes.append(note)
    return c

def music(sound):
    channel1 = mixer.Channel(0)
    sound.set_volume(0.4)
    channel1.play(sound)

def menu(song=None):

    screen.fill(bkg)
    game_surf.fill(clear)
    fx_surf.fill(clear)
    txt_surf.fill(clear)

    key = True
    borderRadius = int(screenSize[0]/20)
    #buttons
    startButn = pygame.Rect(screenSize[0]/20,screenSize[1]*0.4,screenSize[0]/4,screenSize[1]/6)
    how2Butn =  pygame.Rect(screenSize[0]/20,screenSize[1]*.6,screenSize[0]/4,screenSize[1]/6)
    endButn =  pygame.Rect(screenSize[0]/20,screenSize[1]*.8,screenSize[0]/4,screenSize[1]/6)
    pygame.draw.rect(game_surf,darkBkg,startButn, border_top_right_radius=borderRadius)
    pygame.draw.rect(game_surf,darkBkg,how2Butn)
    pygame.draw.rect(game_surf,darkBkg,endButn)
    pygame.draw.rect(game_surf,greenBtn,startButn, width=int(screenSize[0]/100), border_top_right_radius=borderRadius)
    pygame.draw.rect(game_surf,blueBtn,how2Butn, width=int(screenSize[0]/100))
    pygame.draw.rect(game_surf,magentaBtn,endButn, width=int(screenSize[0]/100))

    pygame.draw.polygon(game_surf, darkBkg, [(0, screenSize[1]*0.3),(screenSize[0]*0.38, screenSize[1]*0.3), (0,0)])
    pygame.draw.line(game_surf, "white", (0, screenSize[1]*0.3), (screenSize[0]*0.38, screenSize[1]*0.3), width=int(screenSize[0]/100))
    pygame.draw.line(game_surf, lightBkg, (0, screenSize[1]*0.33), (screenSize[0]*0.29, screenSize[1]*0.33), width=int(screenSize[0]/300))
    pygame.draw.line(game_surf, bkg, (0, screenSize[1]*0.36), (screenSize[0]*0.2, screenSize[1]*0.36), width=int(screenSize[0]/500))

    #text
    sbtn = font4.render("PLAY", False, "white")
    sbtnRect = sbtn.get_rect(center=(screenSize[0]*0.175,screenSize[1]*0.48))
    txt_surf.blit(sbtn, sbtnRect)
    h2btn = font4.render("RULES", False, "white")
    h2btnRect = h2btn.get_rect(center=(screenSize[0]*0.175,screenSize[1]*0.68))
    txt_surf.blit(h2btn, h2btnRect)
    qbtn = font4.render("QUIT", False, "white")
    qbtnRect = qbtn.get_rect(center=(screenSize[0]*0.175,screenSize[1]*0.88))
    txt_surf.blit(qbtn, qbtnRect)
    title = font3.render("UpBeat", False, "white")
    tit_rect = title.get_rect(center=(screenSize[0]*0.23, screenSize[1] / 6))
    txt_surf.blit(title, tit_rect)

    #bkg img
    bkgImg = pygame.image.load('../assets/UpBeat_Temp_Bkg.png')
    bkgImgRect = bkgImg.get_rect(center=(screenSize[0]/2,(screenSize[1]/2)))
    scaleQuantity = screenSize[0]/bkgImgRect.width
    bkgImg = pygame.transform.scale(bkgImg, (bkgImgRect.width*scaleQuantity, bkgImgRect.height*scaleQuantity))
    screen.blit(bkgImg, (0, -1*screenSize[1]/8))

    #compilation
    screen.blit(game_surf, (0, 0))
    screen.blit(txt_surf, (0, 0))
    pygame.display.update()
    if song != None:
        music(song)

    #input
    while key:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if startButn.collidepoint(pygame.mouse.get_pos()):
                    key = False
                    startSound = mixer.Sound('../assets/UpBeat_Start.mp3')
                    channel2 = mixer.Channel(1)
                    startSound.set_volume(0.4)
                    channel2.play(startSound)
                    yeah.set_volume(0.1)
                    channel3.play(yeah)
                    global chosenSong
                    chosenSong = chooseSong()
                elif how2Butn.collidepoint(pygame.mouse.get_pos()):
                    key = False
                    startSound = mixer.Sound('../assets/UpBeat_Start.mp3')
                    channel2 = mixer.Channel(1)
                    startSound.set_volume(0.4)
                    channel2.play(startSound)
                    howToPlay()

                elif endButn.collidepoint(pygame.mouse.get_pos()):
                    scratchSound = mixer.Sound('../assets/UpBeat_Scratch.mp3')
                    channel2 = mixer.Channel(1)
                    scratchSound.set_volume(0.6)
                    channel2.play(scratchSound)
                    pygame.time.wait(300)
                    pygame.quit()
                    sys.exit()
            if event.type==pygame.MOUSEMOTION:
                    pygame.draw.rect(game_surf,darkBkg,startButn, border_top_right_radius=borderRadius)
                    pygame.draw.rect(game_surf,darkBkg,how2Butn)
                    pygame.draw.rect(game_surf,darkBkg,endButn)
                    pygame.draw.rect(game_surf,greenBtn,startButn, width=int(screenSize[0]/100), border_top_right_radius=borderRadius)
                    pygame.draw.rect(game_surf,blueBtn,how2Butn, width=int(screenSize[0]/100))
                    pygame.draw.rect(game_surf,magentaBtn,endButn, width=int(screenSize[0]/100))
                    if startButn.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(game_surf,lightBkg,startButn, border_top_right_radius=borderRadius)
                        pygame.draw.rect(game_surf,green,startButn, width=int(screenSize[0]/100)-1, border_top_right_radius=borderRadius)  
                    elif how2Butn.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(game_surf,lightBkg,how2Butn)
                        pygame.draw.rect(game_surf,blue,how2Butn, width=int(screenSize[0]/100)-1)
                    elif endButn.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(game_surf,lightBkg,endButn)
                        pygame.draw.rect(game_surf,magenta,endButn, width=int(screenSize[0]/100)-1)
                    screen.blit(game_surf, (0, 0))
                    screen.blit(txt_surf, (0, 0))
                    pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scratchSound = mixer.Sound('../assets/UpBeat_Scratch.mp3')
                    channel2 = mixer.Channel(1)
                    scratchSound.set_volume(0.6)
                    channel2.play(scratchSound)
                    pygame.time.wait(300)
                    pygame.quit()
                    sys.exit()

def chooseSong():

    screen.fill(bkg)
    game_surf.fill(clear)
    fx_surf.fill(clear)
    txt_surf.fill(clear)

    key = True
    borderRadius = int(screenSize[0]/20)

    #btns
    song1Btn = pygame.Rect(screenSize[0]*0.075,screenSize[1]*0.5, screenSize[0]*0.4,screenSize[1]*0.45)
    song2Btn = pygame.Rect(screenSize[0]*0.525,screenSize[1]*0.5, screenSize[0]*0.4,screenSize[1]*0.45)
    pygame.draw.rect(game_surf,darkBkg,song1Btn, border_top_left_radius=borderRadius, border_bottom_left_radius=borderRadius)
    pygame.draw.rect(game_surf,darkBkg,song2Btn, border_top_right_radius=borderRadius, border_bottom_right_radius=borderRadius)
    pygame.draw.rect(game_surf,blueBtn,song1Btn, width=int(screenSize[0]/100), border_top_left_radius=borderRadius, border_bottom_left_radius=borderRadius)
    pygame.draw.rect(game_surf,orangeBtn,song2Btn, width=int(screenSize[0]/100), border_top_right_radius=borderRadius, border_bottom_right_radius=borderRadius)

    #text
    esct = font2.render("Press [ESC] to go Back", False, lightBkg)
    esct_rect = esct.get_rect(center=(screenSize[0]*0.125, screenSize[1]*0.025))
    txt_surf.blit(esct, esct_rect)
    sst = font4.render("Select Song:", False, "white")
    sst_rect = sst.get_rect(center=(screenSize[0]*0.5, screenSize[1]*0.375))
    txt_surf.blit(sst, sst_rect)
    s1btn = font4.render("Normal", False, "white")
    s1btnRect = s1btn.get_rect(center=(screenSize[0]*0.275,screenSize[1]*0.6))
    txt_surf.blit(s1btn, s1btnRect)
    s2btn = font4.render("Challenge", False, "white")
    s2btnRect = s2btn.get_rect(center=(screenSize[0]*0.725,screenSize[1]*0.6))
    txt_surf.blit(s2btn, s2btnRect)

    # bkg image
    bkgImg = pygame.image.load('../assets/UpBeat_Crowd.png')
    bkgImgRect = bkgImg.get_rect(center=(screenSize[0]/2,(screenSize[1]/2)))
    scaleQuantity = screenSize[0]/bkgImgRect.width
    bkgImg = pygame.transform.scale(bkgImg, (bkgImgRect.width*scaleQuantity, bkgImgRect.height*scaleQuantity))
    screen.blit(bkgImg, (0, -1*screenSize[1] * 0.6))


    screen.blit(game_surf, (0, 0))
    screen.blit(txt_surf, (0, 0))
    pygame.display.update()

     #input
    while key:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if song1Btn.collidepoint(pygame.mouse.get_pos()):
                    key = False
                    startSound = mixer.Sound('../assets/UpBeat_Start.mp3')
                    channel2 = mixer.Channel(1)
                    startSound.set_volume(0.4)
                    channel2.play(startSound)
                    return s1
                elif song2Btn.collidepoint(pygame.mouse.get_pos()):
                    key = False
                    startSound = mixer.Sound('../assets/UpBeat_Start.mp3')
                    channel2 = mixer.Channel(1)
                    startSound.set_volume(0.4)
                    channel2.play(startSound)
                    return s2
            if event.type==pygame.MOUSEMOTION:
                    pygame.draw.rect(game_surf,darkBkg,song1Btn, border_top_left_radius=borderRadius, border_bottom_left_radius=borderRadius)
                    pygame.draw.rect(game_surf,darkBkg,song2Btn, border_top_right_radius=borderRadius, border_bottom_right_radius=borderRadius)
                    pygame.draw.rect(game_surf,blueBtn,song1Btn, width=int(screenSize[0]/100), border_top_left_radius=borderRadius, border_bottom_left_radius=borderRadius)
                    pygame.draw.rect(game_surf,orangeBtn,song2Btn, width=int(screenSize[0]/100), border_top_right_radius=borderRadius, border_bottom_right_radius=borderRadius)
                    if song1Btn.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(game_surf,lightBkg,song1Btn, border_top_left_radius=borderRadius, border_bottom_left_radius=borderRadius)
                        pygame.draw.rect(game_surf,blue,song1Btn, width=int(screenSize[0]/100)-1, border_top_left_radius=borderRadius, border_bottom_left_radius=borderRadius)
                    elif song2Btn.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(game_surf,lightBkg,song2Btn, border_top_right_radius=borderRadius, border_bottom_right_radius=borderRadius)
                        pygame.draw.rect(game_surf,orange,song2Btn, width=int(screenSize[0]/100)-1, border_top_right_radius=borderRadius, border_bottom_right_radius=borderRadius)
                    screen.blit(game_surf, (0, 0))
                    screen.blit(txt_surf, (0, 0))
                    pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    scratchSound = mixer.Sound('../assets/UpBeat_Scratch.mp3')
                    channel2 = mixer.Channel(1)
                    scratchSound.set_volume(0.6)
                    channel2.play(scratchSound)
                    menu()

def howToPlay():
    screen.fill(darkBkg)
    game_surf.fill(clear)
    fx_surf.fill(clear)
    txt_surf.fill(clear)

    key = True
    global ldm

    ldmBtn = pygame.Rect(screenSize[0]*0.45,screenSize[1]*0.55,screenSize[0]*0.1,screenSize[0]*0.1,)
    pygame.draw.rect(game_surf,gray,ldmBtn)
        #text

    esct = font2.render("Press [ESC] to go Back", False, lightBkg)
    esct_rect = esct.get_rect(center=(screenSize[0]*0.125, screenSize[1]*0.025))
    txt_surf.blit(esct, esct_rect)
    desct = font2.render("LDM", False, "white")
    desct_rect = desct.get_rect(center=(screenSize[0]*0.5, screenSize[1]*0.5))
    txt_surf.blit(desct, desct_rect)
    desct = font2.render("Better Performance", False, "white")
    desct_rect = desct.get_rect(center=(screenSize[0]*0.5, screenSize[1]*0.75))
    txt_surf.blit(desct, desct_rect)
    desct = font2.render("But Worse Visuals", False, "white")
    desct_rect = desct.get_rect(center=(screenSize[0]*0.5, screenSize[1]*0.8))
    txt_surf.blit(desct, desct_rect)

    if ldm == True:
        pygame.draw.rect(game_surf,green,ldmBtn, width=int(screenSize[0]/100))
        ldmbtn = font2.render("ON", False, "white")
    elif ldm == False:
        pygame.draw.rect(game_surf,orange,ldmBtn, width=int(screenSize[0]/100))
        ldmbtn = font2.render("OFF", False, "white")

    ldmbtnRect = ldmbtn.get_rect(center=(screenSize[0]*0.5,screenSize[1]*0.625))
    game_surf.blit(ldmbtn, ldmbtnRect)

    bkgImg = pygame.image.load('../assets/UpBeat_How2.png')
    bkgImgRect = bkgImg.get_rect(center=(screenSize[0]/2,(screenSize[1]/2)))
    scaleQuantity = screenSize[0]/bkgImgRect.width
    bkgImg = pygame.transform.scale(bkgImg, (bkgImgRect.width*scaleQuantity, bkgImgRect.height*scaleQuantity))
    screen.blit(bkgImg, (0, (screenSize[1]-(bkgImgRect.height * scaleQuantity))/2))

    screen.blit(game_surf, (0, 0))
    screen.blit(txt_surf, (0, 0))
    pygame.display.update()

    while key:
        for event in pygame.event.get():
            if event.type==pygame.MOUSEBUTTONDOWN:
                if ldmBtn.collidepoint(pygame.mouse.get_pos()):
                    game_surf.fill(clear)
                    pygame.draw.rect(game_surf,gray,ldmBtn)
                    if ldm == True:
                        ldm = False
                        scratchSound = mixer.Sound('../assets/UpBeat_Scratch.mp3')
                        channel2 = mixer.Channel(1)
                        scratchSound.set_volume(0.6)
                        channel2.play(scratchSound)
                        pygame.draw.rect(game_surf,orange,ldmBtn, width=int(screenSize[0]/100))
                        ldmbtn = font2.render("OFF", False, "white")
                    elif ldm == False:
                        ldm = True
                        startSound = mixer.Sound('../assets/UpBeat_Start.mp3')
                        channel2 = mixer.Channel(1)
                        startSound.set_volume(0.4)
                        channel2.play(startSound)
                        pygame.draw.rect(game_surf,green,ldmBtn, width=int(screenSize[0]/100))
                        ldmbtn = font2.render("ON", False, "white")
                    ldmbtnRect = ldmbtn.get_rect(center=(screenSize[0]*0.5,screenSize[1]*0.625))
                    game_surf.blit(ldmbtn, ldmbtnRect)
                    screen.blit(game_surf, (0, 0))
                    pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    key = False
                    scratchSound = mixer.Sound('../assets/UpBeat_Scratch.mp3')
                    channel2 = mixer.Channel(1)
                    scratchSound.set_volume(0.6)
                    channel2.play(scratchSound)
                    menu()

def startGame(song):
    global running
    running = True
    global bpm
    bpm = song[0][1] / 4
    global noteSpeed
    noteSpeed = song[0][2]
    play = mixer.Sound(song[0][0])
    music(play)

#setup
screen.fill(bkg)
bkg_surf.fill(clear)
game_surf.fill(clear)
fx_surf.fill(clear)
txt_surf.fill(clear)

ldm = False
#LOW DETAIL MODE, Better Performance

#music
menuSong = mixer.Sound('../assets/UpBeat_Menu.mp3')
chosenSong=""
yeah = mixer.Sound('../assets/UpBeat_Yells.mp3')
channel3 = mixer.Channel(2)

#fonts
font1 = pygame.font.Font(None, int(100))
font2 = pygame.font.Font(None, int(50))
font3 = pygame.font.SysFont("impact", int(screenSize[0]/7.5), italic=True)
font4 = pygame.font.SysFont("impact", int(screenSize[0]/12))

menu(menuSong)

screen.fill(bkg)
game_surf.fill(clear)
fx_surf.fill(clear)
txt_surf.fill(clear)

record = Record(screenSize, game_surf)
blueBtn = Button("W", blueBtn, record, screenSize)
orangeBtn = Button("E", orangeBtn, record, screenSize)
greenBtn = Button("S", greenBtn, record, screenSize)
magentaBtn = Button("N", magentaBtn, record, screenSize)
notes = [] #array of all active notes
currentNote = 0 #index number of the most recently spawned note
delZone = pygame.Rect(screenSize[0] / 2, screenSize[1] / 2, 10, 500) #zone where notes get deleted
score = [0, 0, 0]  # actual score percentage, raw score value, total potential score value
streak = 0
    #images
tableImg = pygame.image.load('../assets/UpBeat_Table.png')
tableImg = pygame.transform.scale(tableImg, (screenSize[0], screenSize[0])).convert_alpha()
djImg = pygame.image.load('../assets/UpBeat_DJ.png')
djImg1 = pygame.transform.scale(djImg,(screenSize[1], screenSize[1] * 0.97)).convert_alpha()
djImg2 = pygame.transform.scale(djImg,(screenSize[1], screenSize[1])).convert_alpha()
crowdImg = pygame.image.load('../assets/UpBeat_Crowd.png').convert_alpha()

#start
running = False
startGame(chosenSong)
last_time = time.time()
bkg_surf.fill(pygame.Color(255, 255, 255, 0))
if ldm == False:
    bkg_surf.blit(crowdImg, (0, (-0.57 * screenSize[1]) + (abs(beat - 0.5) * -0.05 * screenSize[1])))
elif ldm == True:
    bkg_surf.blit(djImg1, (0.2 * screenSize[0], -0.17 * screenSize[1]))
    bkg_surf.blit(tableImg, (0, -0.57 * screenSize[1]))
while running==True:
    dt = time.time() - last_time
    # VISUALS ------------------------------------------------------------------------------ #
        # surfaces
    screen.fill(bkg)
    game_surf.fill(pygame.Color(255, 255, 255, 0))
    fx_surf.fill(pygame.Color(255, 255, 255, 0))
    txt_surf.fill(pygame.Color(255, 255, 255, 0))

        # sprites
    if ldm == False:
        if abs((beat*4) - round(beat*4)) < 0.07:
            game_surf.blit(djImg1, (0.2 * screenSize[0], -0.17 * screenSize[1]))
        else:
            game_surf.blit(djImg2, (0.2 * screenSize[0], -0.2 * screenSize[1]))
        game_surf.blit(tableImg, (0, -0.57 * screenSize[1]))

        # draw the records and buttons
    record.draw(gray)

        # score
    sc = font4.render(f"{score[0]}%", False, lightBkg)
    sc_rect = sc.get_rect(center=(screenSize[0] / 6, screenSize[1] / 10))
    txt_surf.blit(sc, sc_rect)

        #cheering
    if streak >= 15:
      if (beatTotal + 1) % 2 <= 0.01:
        vol = 0.2
        if streak < 100:
            vol *= ((streak - 10)/100)
        yeah.set_volume(vol)
        channel3.play(yeah)

    # GAME LOGIC ----------------------------------------------------------------------------- #
        # spawning notes
    if currentNote < len(chosenSong):
        currentNote = progressSequence(currentNote, chosenSong)

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
                scratchSound = mixer.Sound('../assets/UpBeat_Scratch.mp3')
                channel2 = mixer.Channel(1)
                scratchSound.set_volume(0.6)
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
    screen.blit(bkg_surf, (0, 0))
    screen.blit(game_surf, (0, 0))
    screen.blit(fx_surf, (0, 0))
    screen.blit(txt_surf, (0, 0))
    pygame.display.update()
    last_time = time.time()
    mainClock.tick(framerate)
    