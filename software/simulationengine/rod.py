#!/usr/bin/env python
import os,sys,math
import dbus
import dbus.service
import cell

default_max_speed = 1.0
default_scram_speed = 2.0


class rod(dbus.service.Object):
    def __init__(self, bus, mainloop, path_base, x, y, depth, reactor):
        self.object_path = "%s/rod/%d/%d" % (path_base, x, y)
        self.bus_name = dbus.service.BusName('fi.hacklab.reactorsimulator', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)

        self.loop = mainloop
        self.reactor = reactor
        self.x = x
        self.y = y
        self.well_depth = depth
        self.set_depth(float(depth)/2) # This is float so we can keep track of progress in smaller steps, for simulation purposes it will be rounded to int
        self.current_max_speed = default_max_speed
        
        self.water_level = 1.0 # This is basically percentage of the full depth 1.0 means full of water
        self.steam_pressure = 0.0 # In whatever unit we feel is most convinient
        self.avg_temp = 0.0
        
        
        self.cells = []
        for i in range(self.well_depth):
            self.cells.append(cell.cell(bus, self.loop, self.object_path, self.x, self.y, i, self.reactor, self))

        # Final debug statement
        print "%s initialized" % self.object_path

    def tick(self):
        self.cool()  
        self.decay() # This method will update rod avg temp too

    def get_cell_temps(self):
        """Return list of cell temperatures"""
        return map(lambda x: x.temp, self.cells)

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def set_depth(self, depth):
        self.depth = float(depth)
        self.moderator_depth = math.floor(self.depth)
        self.tip_depth = self.moderator_depth+1

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def calc_avg_temp(self):
        """Recalculates the value of the avg_temp property and returns it"""
        self.avg_temp = sum(self.get_cell_temps()) / self.well_depth
        return self.avg_temp;

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def neutron_hit(self, depth):
        """Trigger neutron hit on cell at depth, indices start from zero"""
        self.cells[depth].neutron_hit()

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def decay(self):
        """This is the time-based decay, it will be called by a timer in the reactor"""
        for cell in self.cells:
            cell.decay()
        self.calc_avg_temp()

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def cool(self):
        """This is the time-based cooling, it will be called by a timer in the reactor"""
        for cell in self.cells:
            cell.cool()
        self.calc_avg_temp()

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def report(self):
        for cell in self.cells:
            cell.report()
        # TODO: Report the rod averages
        self.emit_temp(self.avg_temp, self.object_path)
        self.emit_pressure(self.steam_pressure, self.object_path)

    @dbus.service.signal('fi.hacklab.reactorsimulator')
    def emit_temp(self, temp, sender):
        """This emits the temperature of current rod"""
        pass

    @dbus.service.signal('fi.hacklab.reactorsimulator')
    def emit_pressure(self, pressure, sender):
        """This emits the pressure of current rod"""
        pass


if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
