#!/usr/bin/env python
import os,sys
import dbus
import dbus.service

class cell(dbus.service.Object):
    def __init__(self, bus, mainloop, path_base, x, y, depth, reactor, rod):
        self.loop = mainloop
        self.reactor = reactor
        self.object_path = "%s/cell/%d" % (path_base, depth)
        self.bus_name = dbus.service.BusName('fi.hacklab.reactorsimulator', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)

        self.loop = mainloop
        self.reactor = reactor
        self.x = x
        self.y = y
        self.depth = depth
        self.rod = rod
        
        self.temp = 0.0 # Celcius ?

        # Final debug statement
        print "%s initialized" % self.object_path

if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
