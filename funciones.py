# Librerias
import pygame
from pygame.locals import *

def Time_down(time):
    time -= 1

# Cargador imagenes
def Imagen(filename,transparente = False, trs = False):
    image = pygame.image.load(filename)
    if(trs):
        image = image.convert_alpha()
    else:
        image = image.convert()
    if(transparente):
        color = image.get_at((0,0))
        image.set_colorkey(color,RLEACCEL)
    return image
