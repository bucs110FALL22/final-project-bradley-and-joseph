import pygame

#variables
framerate = 30
bpm = 1
beat = 1
beatTotal = 1
noteSpeed = 1
screen = pygame.display.set_mode()
screenSize = pygame.display.get_window_size()
bkg_surf = pygame.Surface((screenSize[0], screenSize[1]), pygame.SRCALPHA)
game_surf = pygame.Surface((screenSize[0], screenSize[1]), pygame.SRCALPHA)
fx_surf = pygame.Surface((screenSize[0], screenSize[1]), pygame.SRCALPHA)
txt_surf = pygame.Surface((screenSize[0], screenSize[1]), pygame.SRCALPHA)