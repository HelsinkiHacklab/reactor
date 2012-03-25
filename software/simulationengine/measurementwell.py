#!/usr/bin/env python
import os,sys
import dbus
import dbus.service


class well(dbus.service.Object):
    def __init__(self, bus, mainloop, path_base, x, y, depth, reactor):
        self.object_path = "%s/mwell/%d/%d" % (path_base, x, y)
        self.bus_name = dbus.service.BusName('fi.hacklab.reactorsimulator', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)

        self.loop = mainloop
        self.reactor = reactor
        self.x = x
        self.y = y
        self.depth = depth

        # Final debug statement
        print "%s initialized" % self.object_path

if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
