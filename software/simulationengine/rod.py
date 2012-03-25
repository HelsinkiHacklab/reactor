#!/usr/bin/env python
import os,sys
import dbus
import dbus.service
import cell


class rod(dbus.service.Object):
    def __init__(self, bus, mainloop, path_base, x, y, depth, reactor):
        self.object_path = "%s/rod/%d/%d" % (path_base, x, y)
        self.bus_name = dbus.service.BusName('fi.hacklab.reactorsimulator', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)

        self.loop = mainloop
        self.reactor = reactor
        self.x = x
        self.y = y
        self.depth = depth
        
        self.cells = []
        for i in range(self.depth):
            self.cells.append(cell.cell(bus, self.loop, self.object_path, self.x, self.y, i, self.reactor, self))

        # Final debug statement
        print "%s initialized" % self.object_path

if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
