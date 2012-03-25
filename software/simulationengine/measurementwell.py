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
        
        self.neutrons_seen = [0 for i in range(self.depth)]
        self.temperatures = [0 for i in range(self.depth)]
        self.avg_temp = 0.0

        

        # Final debug statement
        print "%s initialized" % self.object_path

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def neutron_hit(self, depth):
        """Trigger neutron hit on cell at depth, indices start from zero"""
        self.neutrons_seen[depth] += 1 # keep track of the flow in case we need it
        pass

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def report(self):
        #self.emit_temp(self.temp, self.object_path)
        self.emit_neutrons(self.neutrons_seen, self.object_path)

    @dbus.service.signal('fi.hacklab.reactorsimulator')
    def emit_neutrons(self, neutrons, sender):
        """This emits the temperature of current cell"""
        self.neutrons_seen = [0 for i in range(self.depth)] # reset the count
        pass


if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
