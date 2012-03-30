# A graph visualizer lib using pygame
# zzorn 2012-03-30

import math
import pygame, random
from pygame.locals import *
import textutils
import layout
from colorutils import *
from collections import *
import threading

class data_series_unit():
    """
      Holds data related to one type of unit on a graph.
      The unit normalizes the values to fall within the 0..1 range when rendering, so that they can fit in the window.
      Several series may use the same unit, if they should be comparable to each other.
    """
    def __init__(self, name, color = grey, background_color = black, text_offset = 0, font = textutils.smallFont):
        self.name = name
        self.largest_10 = 0
        self.largest_5  = 0
        self.largest_2  = 0
        self.color = color
        self.reference_line_color = scale_color(desaturate_color(color), 0.6)
        self.background_color = background_color
        self.font = font
        self.text_offset = text_offset
        self.spacing = 1.2
        self.reset_scaling()

    def reset_scaling(self):
        self.max_value = 0.0
        self.min_value = 0.0
        self.scaleY = 1.0
        self.offsetY = 0.0

    def update_scaling(self, value):
        if value > self.max_value:
            self.max_value = float(value)
            self._recalculate_scaling()

        if value < self.min_value:
            self.min_value = float(value)
            self._recalculate_scaling()

    def _recalculate_scaling(self):
        extent = (self.max_value - self.min_value) * self.spacing
        self.scaleY = 1.0 / extent
        self.offsetY = -self.min_value

        # Find positions for reference lines
        max_extent = self.max_value * self.spacing
        self.largest_10 = math.pow(10.0, math.floor(math.log10(max_extent)))

        if self.largest_10 * 5.0 < max_extent:
            self.largest_5 = self.largest_10 * 5.0
        else:
            self.largest_5 = self.largest_10 / 2.0

        if self.largest_10 * 2.0 < max_extent:
            self.largest_2 = self.largest_10 * 2.0
        else:
            self.largest_2 = self.largest_10 / 5.0

    def scale_value(self, value):
        """ Scale the value to range 0..1 """
        return (float(value) + self.offsetY) * self.scaleY

    def scale_value_to_area_y(self, value, area):
        """ Scale the value to range area.bottom, area.top """
        n = self.scale_value(value)
        return int(area.top + area.h - n * area.h)

    def draw(self, surface, area):
        self._draw_line(surface, area, self.largest_10)
        self._draw_line(surface, area, self.largest_5)
        self._draw_line(surface, area, self.largest_2)

    def _draw_line(self, surface, area, num):

        start_x = area.left
        end_x = area.right - self.text_offset

        # Reference line
        y = self.scale_value_to_area_y(num, area)
        surface.lock()
        pygame.draw.line(surface, self.reference_line_color, (start_x, y), (end_x, y), 1)
        surface.unlock()

        # Value and unit
        s = str(num) + "  " + self.name
        textutils.drawTextAtPos(surface, s, end_x, y, self.color, self.background_color, self.font, 1)



class data_series():
    """
      Holds a series of data values with some unit, and provides functions to draw them in a screen area.
      Has a maximum number of values it holds, after that values are discarded.
    """
    def __init__(self, name, color, unit, max_len = 10000):
        self.name = name
        self.color = color
        self.darker_color = scale_color(color, 0.5)
        self._values = deque(maxlen= max_len)
        self.thickness = 2
        self.unit = unit
        self.value_lock = threading.Lock()
        self.value_count = 0
        self._latest_value = 0

    def latest_value(self):
        return self._latest_value

    def add_value(self, value):
        """ Add a value to the series.  Can be called from another thread. """
        self.value_lock.acquire()
        self._values.appendleft(value)
        self.unit.update_scaling(value)
        if self.value_count < self._values.maxlen: self.value_count += 1
        self._latest_value = value
        self.value_lock.release()


    def draw(self, surface, area):
        self.value_lock.acquire()
        if self.value_count > 0:
            xpos = 0
            ypos = 0
            first = True
            for x in range(0, area.w):
                newXpos = area.left + x

                # Get value for x coordinate
                valueIndex = (area.w - x - 1) * self.value_count / area.w
                if valueIndex >= self.value_count: valueIndex = self.value_count - 1  # Clamp
                value = self._values[valueIndex]

                # Scale value to area y size
                newYpos = self.unit.scale_value_to_area_y(value, area)

                # Draw line (except for first point that doesn't have a previous point)
                if first:
                    first = False
                else:
                    pygame.draw.line(surface, self.color, (xpos,ypos), (newXpos,newYpos), self.thickness)

                xpos = newXpos
                ypos = newYpos

        self.value_lock.release()



class graph():
    """
     A graph showing a number of data_series.
    """
    def __init__(self, series):
        self.series = series


    def draw(self, surface, area):
        # Draw unit reference lines
        for serie in self.series:
            serie.unit.draw(surface, area)

        unit_width = 170
        area.w    -= unit_width

        # Draw series
        surface.lock()
        for serie in self.series:
            serie.draw(surface, area)
        surface.unlock()


