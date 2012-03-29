# Utilities for drawing text with pygame
import pygame, random, math, pygame.font
from pygame.locals import *
from colorutils import *

pygame.font.init()
mediumFont = pygame.font.Font(None, 32)

# Draw some text centered on a surface, by default in grey on black
def drawTextCentered(surface, text, color = grey, backgroundColor = black, font = mediumFont):

    # Draw the text to a new image
    textPic = font.render(text, True, color, backgroundColor)

    # Get the size of the text and the surface
    textW, textH = font.size(text)
    surfaceRect = surface.get_rect()

    # Calculate position for the text on the center of the surface
    x = surfaceRect.centerx - textW / 2
    y = surfaceRect.centery - textH / 2

    # Draw the text picture to the middle of the surface
    surface.blit(textPic, (x,y))
    
    