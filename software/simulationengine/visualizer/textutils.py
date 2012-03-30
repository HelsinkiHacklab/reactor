# Utilities for drawing text with pygame
import pygame, random, math, pygame.font
from pygame.locals import *
from colorutils import *

pygame.font.init()
largeFont = pygame.font.Font(None, 32)
mediumFont = pygame.font.Font(None, 24)
smallFont = pygame.font.Font(None, 20)
tinyFont = pygame.font.Font(None, 15)

def drawTextCentered(surface, text, color = grey, background_color = black, font = largeFont):
    """ Draw some text centered on a surface, by default in grey on black """

    # Get surface center
    surfaceRect = surface.get_rect()
    x = surfaceRect.centerx
    y = surfaceRect.centery

    # Draw text
    drawTextAtPos(surface, text, x, y, color, background_color, font)


def font_height(font):
    w, h = font.size("X")
    return h

def drawTextAtPos(surface, text, x, y, color = grey, background_color = black, font = largeFont):
    """ Draw some text centered on the specified location on a surface, by default in grey on black """

    # Create texture pic
    textPic, textW, textH = createText(text, color, background_color, font)

    # Calculate position for the text
    tx = x - textW / 2
    ty = y - textH / 2

    # Draw the text picture to the middle of the surface
    surface.blit(textPic, (tx,ty))

def drawTextInRect(surface, rect, text, color = grey, background_color = black, font = largeFont):
    """ Draw some text left justified in the specified rectangle, by default in grey on black """

    # Create texture pic
    textPic, textW, textH = createText(text, color, background_color, font)

    # Calculate position for the text
    tx = rect.left
    ty = rect.centery - textH / 2

    # Draw the text
    surface.blit(textPic, (tx,ty))


def createText(text, color = grey, background_color = black, font = largeFont):
    """ Create a bitmap with the specified text, and return it along with its width and height """

    # Draw the text to a new image
    textPic = font.render(text, True, color, background_color)

    # Get the size of the text
    textW, textH = font.size(text)

    return textPic, textW, textH

