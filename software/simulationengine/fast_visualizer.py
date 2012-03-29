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
        screenSize = [1024, 256*3]
        pygame.init()
        self.screen = pygame.display.set_mode(screenSize)
        pygame.display.set_caption("Reactor Visualizer")

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


            # Fill screen with black, so that earlier graphics don't show up
            self.screen.fill(grey)

            # Update reactor view
            self.draw()

            # Show the screen we just painted, and hide and start painting on the screen that was just visible
            pygame.display.flip()

        # Clear screen to show immediate response to quit signal (closing can take a second or two if many resources used)
        self.screen.fill(black)
        textutils.drawTextCentered(self.screen, "Reactor visualizer closing")
        pygame.display.flip()

        # Release loaded resources, shut down pygame
        pygame.quit ()


    def draw(self):
        blockSize = 64
        margin = 4
        self.screen.lock()
        for x in self.width_range:
            for y in self.height_range:
                t = self.temperatures[reactor_index(x, y, 3)]
                normalized_temp = t / (t + 200.0)
                red = normalized_temp
                blue = 1.0 - normalized_temp
                color = (255 * red, 0, 255 * blue)
                rect = (x*blockSize+margin, y*blockSize+margin, blockSize-2*margin, blockSize-2*margin)
                pygame.draw.rect(self.screen, color, rect)

        self.screen.unlock()

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


