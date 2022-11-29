import pygame, time

pygame.init()

last_time = time.time()
framerate = 60
bpm = 60
beat = 0
beatTotal = 0

noteSpeed = 5

screen = pygame.display.set_mode()
screenSize = pygame.display.get_window_size()

game_surf = pygame.Surface((screenSize[0], screenSize[1]), pygame.SRCALPHA)
fx_surf = pygame.Surface((screenSize[0], screenSize[1]), pygame.SRCALPHA)
txt_surf = pygame.Surface((screenSize[0], screenSize[1]), pygame.SRCALPHA)

font1 = pygame.font.Font(None, int(100))
font2 = pygame.font.Font(None, int(50))
