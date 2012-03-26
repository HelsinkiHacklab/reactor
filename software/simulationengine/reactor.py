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
max_temp = 1500.0 # This is used in visualizations etc, the max point temperature we are going to see while the reactor has not yet blown up

# It seems that as things get hotter we start lagging behind in our clock or something, at least the visualization starts seeing longer and longer intervalls between report signals

class reactor(dbus.service.Object):
    def __init__(self, bus, mainloop, path_base):
        self.object_path = path_base + '/reactor'
        self.bus_name = dbus.service.BusName('fi.hacklab.reactorsimulator', bus=bus)
        self.bus = bus
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)


        self.loop = mainloop
        self.tick_count = 0
        self.grid_limits = [0,0,0]


        self.avg_temp = 0.0
        self.avg_pressure = 0.0 

        # Final debug statement
        print "%s initialized" % self.object_path

    def in_grid(self, x, y, z):
        """Helper to check if given x,y,z is even in theory inside the reactor"""
        if (   x >= self.grid_limits[0]
            or x < 0):
            return False
        if (   y >= self.grid_limits[1]
            or y < 0):
            return False
        if (   z >= self.grid_limits[2]
            or z < 0):
            return False
        return True

    def load_layout(self, layout, depth):
        self.layout = []
        self.rods = []
        self.mwells = []
        xcount = len(layout)
        ycount = len(layout[0])
        self.grid_limits = [xcount, ycount, depth]
        for x in range(xcount):
            col = []
            for y in range(ycount):
                # We have a controllable rod here
                if (layout[x][y] == '*'):
                    col.append(rod.rod(self.bus, self.loop, self.object_path, x, y, depth, self))
                    self.rods.append(col[y])
                    continue
                if (layout[x][y] == '#'):
                    col.append(measurementwell.well(self.bus, self.loop, self.object_path, x, y, depth, self))
                    self.mwells.append(col[y])
                    continue
                # Default case is to skip
                col.append(None)
            self.layout.append(col)
        self.rod_count = len(self.rods)

    def tick(self):
        self.tick_count += 1

        # Call the decay methods on the rods
        for rod in self.rods:
            rod.tick() # This method will update rod avg temp
        
        # after tiher tick actions blend temperatures
        for rod in self.rods:
            rod.calc_blend_temp()
        for well in self.mwells:
            well.calc_blend_temp()

        # after tiher tick actions blend temperatures
        for rod in self.rods:
            rod.sync_blend_temp() # This method will update rod avg temp
        for well in self.mwells:
            well.sync_blend_temp()

        # Update the reactor average values
        self.calc_avg_temp()
        self.calc_avg_pressure()
        
        # TODO: check if we're within set limits

        # Trigger reports at each tick
        self.report()
        # return true to keep ticking
        print "Reactor tick #%d done" % self.tick_count
        return True

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def report(self):
        """This will trigger report methods for everything else, they will emit signals"""

        for rod in self.rods:
            rod.report()

        for well in self.mwells:
            well.report()


    def get_rod_temps(self):
        """Return list of rod temperatures, NOTE: does not trigger recalculation on the rod so might return old data"""
        return map(lambda x: x.avg_temp, self.rods)

    def get_rod_pressures(self):
        """Return list of rod pressures, NOTE: does not trigger recalculation on the rod so might return old data"""
        return map(lambda x: x.steam_pressure, self.rods)

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def calc_avg_temp(self):
        """Recalculates the value of the avg_temp property and returns it"""
        self.avg_temp = sum(self.get_rod_temps()) / self.rod_count
        return self.avg_temp;

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def calc_avg_pressure(self):
        """Recalculates the value of the avg_pressure property and returns it"""
        self.avg_pressure = sum(self.get_rod_pressures()) / self.rod_count
        return self.avg_pressure;


if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
