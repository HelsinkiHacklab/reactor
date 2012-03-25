#!/usr/bin/env python
import os,sys
import dbus
import dbus.service

import rod, measurementwell

# Layout of the generator, '*' is a rod place, '#' is automatic whatever place, ' ' is nothing
default_layout = [[' ', ' ', '*', '*', '*', ' ', ' '],
                  [' ', '*', '#', '*', '*', '*', ' '],
                  ['*', '*', '*', '*', '*', '#', '*'],
                  ['*', '*', '*', '*', '*', '*', '*'],
                  ['*', '#', '*', '*', '*', '*', '*'],
                  [' ', '*', '*', '*', '#', '*', ' '],
                  [' ', ' ', '*', '*', '*', ' ', ' ']] 

# Depth of each rod well
default_depth = 7

class reactor(dbus.service.Object):
    def __init__(self, bus, mainloop, path_base):
        self.object_path = path_base + '/reactor'
        self.bus_name = dbus.service.BusName('fi.hacklab.reactorsimulator', bus=bus)
        self.bus = bus
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)


        self.loop = mainloop

        # Final debug statement
        print "%s initialized" % self.object_path

    def load_layout(self, layout, depth):
        self.layout = []
        xcount = len(layout)
        ycount = len(layout[0])
        for x in range(xcount):
            col = []
            for y in range(ycount):
                # We have a controllable rod here
                if (layout[x][y] == '*'):
                    col.append(rod.rod(self.bus, self.loop, self.object_path, x, y, depth, self))
                if (layout[x][y] == '#'):
                    col.append(measurementwell.well(self.bus, self.loop, self.object_path, x, y, depth, self))
                # Default case is to skip
                col.append(None)
                
                


if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
