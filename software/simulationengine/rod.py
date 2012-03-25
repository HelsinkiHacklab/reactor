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
        
        self.water_level = 1.0 # This is basically percentage of the full depth 1.0 means full of water
        self.steam_pressure = 0.0 # In whatever unit we feel is most convinient
        self.avg_temp = 0.0
        
        
        self.cells = []
        for i in range(self.depth):
            self.cells.append(cell.cell(bus, self.loop, self.object_path, self.x, self.y, i, self.reactor, self))

        # Final debug statement
        print "%s initialized" % self.object_path

    def get_cell_temps(self):
        """Return list of cell temperatures"""
        return map(lambda x: x.temp, self.cells)

    def calc_avg_temp(self):
        """Recalculates the value of the avg_temp property and returns it"""
        self.avg_temp = sum(self.get_cell_temps()) / self.depth
        return self.avg_temp;


if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
