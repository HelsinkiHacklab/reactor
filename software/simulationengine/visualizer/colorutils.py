# Utilities for colors
import pygame, random, math, pygame.font
from pygame.locals import *

black = (0,0,0)
grey = (128, 128, 128)
white = (255, 255, 255)
red = (176, 23, 31)
yellow = (200, 200, 0)
darkred = (139, 0, 0)

orange = (200, 128, 0)
warmorange = (255, 128, 0)
coldorange = (200, 160, 0)

purple = (100, 0, 200)
coldpurple = (80, 0, 240)
warmpurple = (140, 0, 180)


blue = (0, 0, 238)
royalblue = (72, 118, 255)
cobaltblue = (61, 89, 171)
steelblue = (92, 172, 238)
greyblue = (141, 182, 205)
darkgreyblue = (96/2, 123/2, 139/2)
green = (0, 128, 0)

brightgreen = (0, 200, 0)


def scale_color(color, scale):
    r = color[0] * scale
    g = color[1] * scale
    b = color[2] * scale
    return clamp_color((r, g, b))

def mix_color(color1, color2, amount = 0.5):
    inv_amount = 1.0 - amount
    r = inv_amount * color1[0] + amount * color2[0]
    g = inv_amount * color1[1] + amount * color2[1]
    b = inv_amount * color1[2] + amount * color2[2]
    return clamp_color((r, g, b))

def desaturate_color(color, amount = 0.5):
    level = (color[0] + color[1] + color[2]) / 3.0
    return mix_color(color, (level, level, level), amount)


def clamp_color(color):
    r = color[0]
    g = color[1]
    b = color[2]
    return (_clamp(r), _clamp(g), _clamp(b))

def _clamp(v):
    if v < 0: return 0
    elif v > 255: return 255
    else: return v
