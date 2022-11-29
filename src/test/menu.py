import pygame
from colors import *
from var import *
pygame.init()
#class Menu:
    #def __init__(self,color,beat,speed,surface):
    #Will Make the menu
        #self.color = color
        #self.beat = beat
        #self.speed = speed
        #self.surface = surface
def Menu():  
    window = pygame.display.set_mode((500,500))   
    window.fill(magenta)   
    pygame.draw.rect(window,(clear),[100,25,300,100],0)   
    #Will be the play botton   
    pygame.draw.rect(window,(clear),[100,150,300,100],0)   
    #Will be the settings botton so will go into another menu with volume   
    pygame.draw.rect(window,(clear),[100,275,300,100],0)   
    #Will go into credits   
    pygame.draw.rect(window,(clear),[100,425,300,100],0)   
    #Will brake   
    pygame.display.update()   
    pygame.time.wait(5000)
Menu()