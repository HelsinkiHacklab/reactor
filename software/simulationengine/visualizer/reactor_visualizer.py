# Faster visualizer using pygame
# zzorn 2012-03-29

#!/usr/bin/env python
from __future__ import with_statement
import os,sys,time
import math
import reactor
import threading

import dbus
import dbus.service

import pygame, random
from pygame.locals import *

import textutils
import layout
import graph
from colorutils import *

def cell_index(x, y, z):
    return x + y*reactor.reactor_width + z*reactor.reactor_width*reactor.reactor_height

def rod_index(x, y):
    return x + y*reactor.reactor_width


class string_view():
    def __init__(self, host, property, title, unit, color=grey, background_color=black, font=textutils.mediumFont):
        self.host = host
        self.property = property
        self.title = title
        self.unit = unit
        self.color = color
        self.background_color = background_color
        self.font = font

    def height(self):
        return textutils.font_height(self.font)

    def draw(self, surface, rect):
        value = str(getattr(self.host, self.property))
        text = self.title + ":  " + value + "  " + self.unit
        textutils.drawTextInRect(surface, rect, text, self.color, self.background_color, self.font)

class number_view():
    def __init__(self, host, property, title, unit, decimals = 0, color=grey, background_color=black, font=textutils.mediumFont):
        self.host = host
        self.property = property
        self.title = title
        self.unit = unit
        self.decimals = decimals
        self.color = color
        self.background_color = background_color
        self.font = font

    def height(self):
        return textutils.font_height(self.font)

    def draw(self, surface, rect):
        value = getattr(self.host, self.property)
        text = self.title + ":  " + (("%0."+str(self.decimals)+"f") % value) + "  " + self.unit
        textutils.drawTextInRect(surface, rect, text, self.color, self.background_color, self.font)

class series_view():
    def __init__(self, data_series, decimals = 0, color=grey, background_color=black, font=textutils.mediumFont):
        self.data_series = data_series
        self.decimals = decimals
        self.color = color
        self.background_color = background_color
        self.font = font

    def height(self):
        return textutils.font_height(self.font)

    def draw(self, surface, rect):
        value = self.data_series.latest_value()
        text = self.data_series.name + ":  " + \
               (("%0."+str(self.decimals)+"f") % value) + "  " + \
               self.data_series.unit.name

        # Draw label indicator
        surface.lock()
        m1 = 0
        m2 = 1
        s1 = rect.height - 2 * m1
        s2 = rect.height - 2 * m2
        pygame.draw.rect(surface, self.data_series.darker_color, (rect.left+m1, rect.top+m1, s1, s1))
        pygame.draw.rect(surface, self.data_series.color,        (rect.left+m2, rect.top+m2, s2, s2))
        surface.unlock()

        # Draw label
        offset = rect.height + 6
        rect.left += offset
        rect.w    -= offset
        textutils.drawTextInRect(surface, rect, text, self.color, self.background_color, self.font)

class boolean_view():
    def __init__(self, host, property, title, true_text, false_text, true_color=grey, false_color=grey, background_color=black, font=textutils.mediumFont):
        self.host = host
        self.property = property
        self.title = title
        self.true_text = true_text
        self.false_text = false_text
        self.true_color = true_color
        self.false_color = false_color
        self.background_color = background_color
        self.font = font

    def height(self):
        return textutils.font_height(self.font)

    def draw(self, surface, rect):
        value = getattr(self.host, self.property)
        if value:
            text = self.title + ":  " + self.true_text
            textutils.drawTextInRect(surface, rect, text, self.true_color, self.background_color, self.font)
        else:
            text = self.title + ":  " + self.false_text
            textutils.drawTextInRect(surface, rect, text, self.false_color, self.background_color, self.font)



class reactor_listener(threading.Thread):
    def __init__(self, bus, loop):
        threading.Thread.__init__(self)
        self.bus = bus
        self.loop = loop
        self.running = True

        self.vertical_orientation = False
        self.initial_screen_size = [1200, 800]

        self.name = "Reactor Core Visualizer"
        self.helptext = "ESC: Quit,  SPACE: Toggle layout,  BACKSPACE: Reset visualization state"
        self.background_color = black

        self.reset_state()

        # Start listening to reactor state reports from DBUS
        self.bus.add_signal_receiver(self.temperature_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_temp")
        self.bus.add_signal_receiver(self.neutron_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_neutrons")
        self.bus.add_signal_receiver(self.pressure_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_pressure")
        self.bus.add_signal_receiver(self.avg_pressure_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_avg_pressure")
        self.bus.add_signal_receiver(self.max_pressure_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_max_pressure")
        self.bus.add_signal_receiver(self.avg_temperature_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_avg_temperature")
        self.bus.add_signal_receiver(self.max_temperature_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_max_temperature")
        self.bus.add_signal_receiver(self.power_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_power")
        self.bus.add_signal_receiver(self.rod_position_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_depth")
        self.bus.add_signal_receiver(self.blowout_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_blowout")
        self.bus.add_signal_receiver(self.redalert_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert")
        self.bus.add_signal_receiver(self.redalert_reset_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert_reset")
        self.bus.add_signal_receiver(self.cell_melted_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_cell_melted")

        # TODO: Listen to DBUS quit and restart signals

    def reset_state(self, *args):
        """ Initializes or resets the visualized simulation state. Should be called when simulation is restarted. """
        # Create arrays used to keep track of the current reactor state
        reactor_floor_size = reactor.reactor_width * reactor.reactor_height
        self.temperatures = [0.0] * reactor.reactor_cube_size
        self.neutrons     = [0.0] * reactor.reactor_cube_size
        self.pressure     = [0.0] * reactor_floor_size
        self.rod_position = [0.0] * reactor_floor_size
        self.rod_velocity = [0.0] * reactor_floor_size
        self.operational  = [True] * reactor.reactor_cube_size
        self.power        = 0.0
        self.avg_pressure = 0.0
        self.max_pressure = 0.0
        self.avg_temperature = 0.0
        self.max_temperature = 0.0
        self.blown_up     = False
        self.red_alert    = False

        self.width_range  = range(0, reactor.reactor_width)
        self.height_range  = range(0, reactor.reactor_height)
        self.depth_range  = range(0, reactor.reactor_depth)

        # Graphing
        power_unit = graph.data_series_unit("MW", brightgreen, self.background_color)
        temperature_unit = graph.data_series_unit("C", orange, self.background_color, 50)
        pressure_unit = graph.data_series_unit("atm", purple, self.background_color, 100)
        self.power_series = graph.data_series("Power Output", brightgreen, power_unit)
        self.avg_temp_series = graph.data_series("Average Temperature", coldorange, temperature_unit)
        self.max_temp_series = graph.data_series("Max Temperature", warmorange, temperature_unit)
        self.avg_pressure_series = graph.data_series("Average Pressure", coldpurple, pressure_unit)
        self.max_pressure_series = graph.data_series("Max Pressure", warmpurple, pressure_unit)
        self.graph = graph.graph([
            self.power_series,
            self.avg_temp_series,
            self.max_temp_series,
            self.avg_pressure_series,
            self.max_pressure_series
        ])

        # Create some views
        self.status_views = [
            boolean_view(self, "blown_up", "Status", "Meltdown", "Operational", orange, grey, self.background_color),
            boolean_view(self, "red_alert", "Alerts", "RED ALERT", "None", red, grey, self.background_color),
            series_view(self.power_series, background_color=self.background_color),
            series_view(self.avg_temp_series, background_color=self.background_color),
            series_view(self.max_temp_series, background_color=self.background_color),
            series_view(self.avg_pressure_series, 2, background_color=self.background_color),
            series_view(self.max_pressure_series, 2, background_color=self.background_color)
        ]



    def run(self):
        # Setup screen
        pygame.init()
        self.screen = pygame.display.set_mode(self.initial_screen_size, pygame.RESIZABLE)
        pygame.display.set_caption(self.name)

        # Start mainloop
        self.mainloop()
        
        # Stop the dbus/glib mainloop too
        self.loop.quit()


    def mainloop(self):
        clock = pygame.time.Clock()

        while (self.running):
            # Run at 40 frames per second
            frameDurationSeconds = clock.tick(40) * 0.001 # Returns milliseconds since last call, convert to seconds

            # Check if ESC was pressed or window closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                    self.quit()
                elif event.type == pygame.KEYDOWN and (event.key == K_BACKSPACE or event.key == K_DELETE):
                    self.reset_state()
                elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
                    # Toggle orientation
                    self.vertical_orientation = not self.vertical_orientation
                    #screenW, screenH = self.screen.get_size()
                    #self.screen = pygame.display.set_mode([screenH, screenW],pygame.RESIZABLE)
                elif event.type == pygame.VIDEORESIZE:
                    # Screen was resized, resize display
                    new_size = [event.w, event.h]
                    self.screen = pygame.display.set_mode(new_size,pygame.RESIZABLE)

            # Fill screen, so that earlier graphics don't show up
            self.screen.fill(self.background_color)

            # Update reactor view
            self.draw()

            # Show the screen we just painted, and hide and start painting on the screen that was just visible
            pygame.display.flip()

        # Clear screen to show immediate response to quit signal (closing can take a second or two)
        self.screen.fill(black)
        textutils.drawTextCentered(self.screen, self.name + " Closing...")
        pygame.display.flip()

        # Release loaded resources, shut down pygame
        pygame.quit ()


    def draw(self):

        # Margin sizes, in pixels
        displayMargin = 12

        # Get screen rectangle
        base = self.screen.get_rect()
        base = base.inflate(-displayMargin*2, -displayMargin*2)

        # Calculate view positions
        view_margin = 10
        helpH = 10
        mainH = base.h - helpH

        # Setup layout
        mainRect, helpRect = layout.split_absolute(base, (mainH, mainH), True, view_margin)
        if self.vertical_orientation:
            # A layout where the reactor slices are placed vertically
            generalRect, sliceRect = layout.split_proportional(mainRect, (0.6, 0.6), False, view_margin)
            generalRect2, graphRect = layout.split_absolute(generalRect, (240, 240), True, view_margin)
            statusRect, pressureRect = layout.split_absolute(generalRect2, (260, 260), False, view_margin)
            tempRect, neutronRect = layout.split_rect(sliceRect, 2, False, view_margin)
        else:
            # A layout where the reactor slices are placed horizontally
            generalRect, sliceRect = layout.split_proportional(mainRect, (0.4, 0.4), True, view_margin)
            statusRect, generalRect2 = layout.split_absolute(generalRect, (260, 240), False, view_margin)
            graphRect, pressureRect = layout.split_proportional(generalRect2, (0.7, 0.7), False, view_margin)
            tempRect, neutronRect = layout.split_rect(sliceRect, 2, True, view_margin)

        # Draw the different views
        self._draw_views("Status", self.status_views, statusRect)
        self._draw_graph("Graphs", self.graph, graphRect)
        self._draw_layer("Pressure", self.pressure, 0, 10.0, pressureRect, False, white, textutils.largeFont)
        self._draw_layers("Temperature", self.temperatures, 300.0, tempRect)
        self._draw_layers("Neutron Flux", self.neutrons, 1.0, neutronRect)
        textutils.drawTextInRect(self.screen, helpRect, self.helptext, background_color=self.background_color, font=textutils.smallFont)



    def _draw_graph(self, title, graph, rect, label_color = white, label_font = textutils.largeFont):
        # Create title and get remaining space
        content = layout.make_titled_rect(self.screen, rect, title, label_color, self.background_color, label_font, 8, 4)

        # Draw graph
        graph.draw(self.screen, content)


    def _draw_views(self, title, views, rect, label_color = white, label_font = textutils.largeFont):
        # Create title and get remaining space
        content = layout.make_titled_rect(self.screen, rect, title, label_color, self.background_color, label_font, 8, 4)

        # Layout the views
        num = len(views)
        view_separation = 6
        height = sum(map(lambda v: v.height(), views)) + view_separation * (num - 1)
        if content.h > height: content.h = height
        view_rects = layout.split_rect(content, num, True, view_separation)

        # Draw views
        for i in range(0, num):
            view = views[i]
            view.draw(self.screen, view_rects[i])


    def _draw_layers(self, name, data_cube, scale, rect, label_color = white, label_font = textutils.largeFont):
        # Create title and get remaining space
        content = layout.make_titled_rect(self.screen, rect, name, label_color, self.background_color, label_font)

        # Calculate layer positions
        layer_separation = 2
        layer_rects = layout.split_rect(content, reactor.reactor_depth, self.vertical_orientation, layer_separation)

        # Draw layers
        for z in self.depth_range:
            label = "Level " + str(z+1)
            self._draw_layer(label, data_cube, z, scale, layer_rects[z])


    def _draw_layer(self, label, data_cube, z, scale, rect, show_broken_cells = True, label_color = grey, label_font = textutils.mediumFont):

        # Create title and get remaining space
        content = layout.make_titled_rect(self.screen, rect, label, label_color, self.background_color, label_font)

        # Calculate cell size
        cellW = int(content.w / reactor.reactor_width)
        cellH = int(content.h / reactor.reactor_height)


        # Check if we should draw cell labels
        draw_labels = cellW > 32 and cellH > 12
        if not draw_labels: self.screen.lock()

        # Draw cells
        for x in self.width_range:
            for y in self.height_range:
                # Calculate location
                xpos = int(content.left + x * cellW)
                ypos = int(content.top  + y * cellH)

                # Draw
                self._draw_cell(data_cube, x, y, z, scale, xpos, ypos, cellW, cellH, draw_labels, show_broken_cells)

        if not draw_labels: self.screen.unlock()



    def _draw_cell(self, data_cube, x, y, z, scale, xpos, ypos, w, h, draw_labels, show_broken_cells = True):
        if reactor.cell_type(x, y) != ' ':
            index = cell_index(x, y, z)

            # Get temperature
            t = data_cube[index]

            # Calculate color for temp
            normalized_temp = t / (t + scale)
            red = normalized_temp
            blue = 1.0 - normalized_temp
            green = (normalized_temp - 0.5) *2
            if green < 0: green = 0
            color = (255*red, 255*green, 255*blue)

            # Draw cell
            if draw_labels: self.screen.lock()
            pygame.draw.rect(self.screen, color, (xpos, ypos, w-1, h-1))
            if draw_labels: self.screen.unlock()

            # Draw label, if there is room for it
            if draw_labels:
                label = reactor.cell_name(x, y)
                cx = xpos + w/2
                cy = ypos + h/2
                textutils.drawTextAtPos(self.screen, label, cx, cy, black, color, textutils.tinyFont)

            # Cross over if melted
            if show_broken_cells and not self.operational[index]:
                if draw_labels: self.screen.lock()
                crossover_thickness = 2
                pygame.draw.line(self.screen, black, (xpos,ypos), (xpos+w-1,ypos+h-1), crossover_thickness)
                pygame.draw.line(self.screen, black, (xpos+w-1,ypos), (xpos,ypos+h-1), crossover_thickness)
                if draw_labels: self.screen.unlock()


    def quit(self, *args):
        self.running = False
        self.loop.quit()



    def temperature_report(self, x, y, temperature, sender):
        for z in self.depth_range:
            self.temperatures[cell_index(x, y, z)] = temperature[z]

    def neutron_report(self, x, y, neutrons, sender):
        for z in self.depth_range:
            self.neutrons[cell_index(x, y, z)] = neutrons[z]

    def pressure_report(self, x, y, pressure, sender):
        self.pressure[rod_index(x, y)] = pressure

    def avg_pressure_report(self, pressure, sender):
        self.avg_pressure = pressure
        self.avg_pressure_series.add_value(pressure)

    def max_pressure_report(self, pressure, sender):
        self.max_pressure = pressure
        self.max_pressure_series.add_value(pressure)

    def avg_temperature_report(self, temperature, sender):
        self.avg_temperature = temperature
        self.avg_temp_series.add_value(temperature)

    def max_temperature_report(self, temperature, sender):
        self.max_temperature = temperature
        self.max_temp_series.add_value(temperature)

    def power_report(self, power, sender):
        self.power = power
        self.power_series.add_value(power)

    def rod_position_report(self,  x, y, depth, velocity, sender):
        index = rod_index(x, y)
        self.rod_position[index] = depth
        self.rod_velocity[index] = velocity

    def blowout_report(self, sender):
        self.blown_up = True

    def redalert_reset_report(self, sender):
        self.red_alert = False

    def redalert_report(self, sender):
        self.red_alert = True

    def cell_melted_report(self, x, y, z, sender):
        self.operational[cell_index(x, y, z)] = False




if __name__ == '__main__':
    print "Use visualizer_launcher.py"
    sys.exit(1)


