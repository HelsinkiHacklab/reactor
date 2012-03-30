import pygame
from pygame.locals import *
import math

import textutils
from colorutils import *

# Layout utilities, based on pygame rect
def split_rect(rect, number, vertical, separation=0):
    result = []
    if vertical:
        h = rect.h / number
        top = rect.top
        for i in range(0, number):
            r = rect.copy()
            r.top = top + separation
            r.h = h - separation * 2
            result.append(r)
            top += h
    else:
        w = rect.w / number
        left = rect.left
        for i in range(0, number):
            r = rect.copy()
            r.left = left + separation
            r.w = w - separation * 2
            result.append(r)
            left += w

    return result

def split_proportional(rect, (first_size_w, first_size_h), vertical, separation=0):
    return split_absolute(rect, (rect.w * first_size_w, rect.h * first_size_h) , vertical, separation)

def split_absolute(rect, (first_size_w, first_size_h), vertical, separation=0):
    if vertical:
        h1 = first_size_h

        r1 = rect.copy()
        r2 = rect.copy()

        r1.h = abs(h1 - separation)
        r2.h = abs(rect.h - h1 - separation)
        r2.top = r1.bottom + separation * 2

        return r1, r2
    else:
        w1 = first_size_w

        r1 = rect.copy()
        r2 = rect.copy()

        r1.w = abs(w1 - separation)
        r2.w = abs(rect.w - w1 - separation)
        r2.left = r1.right + separation * 2

        return r1, r2


def make_titled_rect(surface, rect, title, color=grey, background_color=black, font=textutils.mediumFont, content_margin = 4, title_separation = 0):
    """ Draws a title at the top of the rect, and returns a rectangle with space for the content. """

    # Create text pic
    text_pic, text_w, text_h = textutils.createText(title, color, background_color, font)

    # Calculate position for the text
    tx = rect.centerx - text_w / 2
    ty = rect.top

    # Draw the text picture to the top of the surface
    surface.blit(text_pic, (tx,ty))

    # Calculate content size
    content = rect.copy()
    content.top += text_h + title_separation
    content.h   -= text_h + title_separation
    content.inflate_ip(-2*content_margin, -2*content_margin)
    return content
