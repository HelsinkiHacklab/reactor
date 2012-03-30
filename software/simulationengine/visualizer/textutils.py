# Utilities for drawing text with pygame
import pygame, random, math, pygame.font
from pygame.locals import *
from colorutils import *

pygame.font.init()
mediumFont = pygame.font.Font(None, 32)
smallFont = pygame.font.Font(None, 15)

def drawTextCentered(surface, text, color = grey, backgroundColor = black, font = mediumFont):
    """ Draw some text centered on a surface, by default in grey on black """

    # Get surface center
    surfaceRect = surface.get_rect()
    x = surfaceRect.centerx
    y = surfaceRect.centery

    # Draw text
    drawTextAtPos(surface, text, x, y, color, backgroundColor, font)


def drawTextAtPos(surface, text, x, y, color = grey, backgroundColor = black, font = mediumFont):
    """ Draw some text centered on the specified location on a surface, by default in grey on black """

    # Draw the text to a new image
    textPic = font.render(text, True, color, backgroundColor)

    # Get the size of the text
    textW, textH = font.size(text)

    # Calculate position for the text
    tx = x - textW / 2
    ty = y - textH / 2

    # Draw the text picture to the middle of the surface
    surface.blit(textPic, (tx,ty))

