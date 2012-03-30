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
from colorutils import *

def reactor_index(x, y, z):
    return x + y*reactor.reactor_width + z*reactor.reactor_width*reactor.reactor_height

class reactor_listener(threading.Thread):
    def __init__(self, bus):
        threading.Thread.__init__(self)
        self.bus = bus
        self.running = True

        self.vertical_orientation = True

        self.name = "Reactor Core Visualizer"

        # Create arrays used to keep track of the current reactor state
        self.temperatures =  [0.0] * reactor.reactor_cube_size
        self.neutrons     =  [0.0] * reactor.reactor_cube_size
        self.width_range  = range(0, reactor.reactor_width)
        self.height_range  = range(0, reactor.reactor_height)
        self.depth_range  = range(0, reactor.reactor_depth)

        # Start listening to reactor state reports from DBUS
        self.bus.add_signal_receiver(self.temperature_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_temp")
        #self.bus.add_signal_receiver(self.neutron_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_neutrons")

        # TODO: Listen to DBUS quit signal

    def run(self):
        # Setup screen
        screenSizeX = 400
        screenSizeY = 800
        pygame.init()
        self.screen = pygame.display.set_mode([screenSizeX, screenSizeY], pygame.RESIZABLE)
        pygame.display.set_caption(self.name)

        # Start mainloop
        self.mainloop()


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
                elif event.type == pygame.KEYDOWN and event.key == K_SPACE:
                    # Toggle orientation
                    self.vertical_orientation = not self.vertical_orientation
                    screenW, screenH = self.screen.get_size()
                    self.screen = pygame.display.set_mode([screenH, screenW],pygame.RESIZABLE)
                elif event.type == pygame.VIDEORESIZE:
                    # Screen was resized, resize display
                    new_size = [event.w, event.h]
                    self.screen = pygame.display.set_mode(new_size,pygame.RESIZABLE)

            # Fill screen, so that earlier graphics don't show up
            self.screen.fill(black)

            # Update reactor view
            self.draw()

            # Show the screen we just painted, and hide and start painting on the screen that was just visible
            pygame.display.flip()

        # Clear screen to show immediate response to quit signal (closing can take a second or two if many resources used)
        self.screen.fill(black)
        textutils.drawTextCentered(self.screen, self.name + " Closing")
        pygame.display.flip()

        # Release loaded resources, shut down pygame
        pygame.quit ()


    def draw(self):
        # Margin sizes, in pixels if integers
        layerMargin = 6
        displayMargin = 12

        # Get current screensize
        screenW, screenH = self.screen.get_size()
        usableScreenX = 1.0 * screenW - displayMargin * 2
        usableScreenY = 1.0 * screenH - displayMargin * 2

        # Layer sizes
        usableLayerX = usableScreenX - 2 * layerMargin
        usableLayerY = usableScreenY - 2 * layerMargin
        layerStepX = 0
        layerStepY = 0
        if self.vertical_orientation:
            layerStepY = usableScreenY / reactor.reactor_depth
            usableLayerY = layerStepY - 2 * layerMargin
        else:
            layerStepX = usableScreenX / reactor.reactor_depth
            usableLayerX = layerStepX - 2 * layerMargin

        # Block sizes and margins
        blockStepX = int(usableLayerX / reactor.reactor_width)
        blockStepY = int(usableLayerY / reactor.reactor_height)

        # Upper left corner
        layerStartX = int(displayMargin + layerMargin)
        layerStartY = int(displayMargin + layerMargin)


        layerX = layerStartX
        layerY = layerStartY
        for z in self.depth_range:
            for x in self.width_range:
                for y in self.height_range:
                    # Calculate location
                    xpos = int(layerX + x*blockStepX)
                    ypos = int(layerY + y*blockStepY)

                    # Draw
                    self._draw_cell(x, y, z, xpos, ypos, blockStepX, blockStepY)

            layerX += int(layerStepX)
            layerY += int(layerStepY)




    def _draw_cell(self, x, y, z, xpos, ypos, w, h):
        if reactor.cell_type(x, y) != ' ':
            # Get temperature
            t = self.temperatures[reactor_index(x, y, z)]

            # Calculate color for temp
            normalized_temp = t / (t + 200.0)
            red = normalized_temp
            blue = 1.0 - normalized_temp
            green = (normalized_temp - 0.5) *2
            if green < 0: green = 0
            color = (255*red, 255*green, 255*blue)

            # Draw cell
            self.screen.lock()
            pygame.draw.rect(self.screen, color, (xpos, ypos, w-1, h-1))
            self.screen.unlock()

            # Draw label, if there is room for it
            if w > 32 and h > 12:
                label = reactor.cell_name(x, y)
                cx = xpos + w/2
                cy = ypos + h/2
                textutils.drawTextAtPos(self.screen, label, cx, cy, black, color, textutils.smallFont)



    def quit(self):
        self.running = False



    def temperature_report(self, x, y, temperature, sender):
        for z in self.depth_range:
            self.temperatures[reactor_index(x, y, z)] = temperature[z]

    def neutron_report(self, x, y, neutrons, sender):
        for z in self.depth_range:
            self.neutrons[reactor_index(x, y, z)] = neutrons[z]




if __name__ == '__main__':
#    print "Use visualizer_launcher.py"
#    sys.exit(1)
    import dbus.mainloop.glib, gobject
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    loop = gobject.MainLoop()
    listener = reactor_listener(bus)

    # Run visualizer in own thread
    listener.start()

    # TODO: Add some nicer way to exit than ctrl-c

    loop.run()


