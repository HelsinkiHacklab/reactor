#!/usr/bin/env python
import os,sys,random
import dbus
import dbus.service

# Tuning parameters
neutron_hit_temp_increase = 0.5
cool_temp_decrease = 0.1

# Initial inoform 3D probability of causing neutron_hit() in neighbour
neutron_hit_size = 3 # Grid size, changin this is ill-adviced
neutron_hit_p = [[[ 0.01 for val in range(neutron_hit_size)] for col in range(neutron_hit_size)] for row in range(neutron_hit_size)]
neutron_hit_p[1][1][1] = 0.0 # We're in the center, easiest way is to set p to zero



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

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def decay(self):
        """This is the time-based decay, it will be called by a timer in the reactor"""
        # TODO:Check rid position, if control rod is past us we cannot decay (PONDER: or do it in the neutron_hit() method ??)
        self.neutron_hit()

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def cool(self):
        """This is the time-based cooling, it will be called by a timer in the reactor"""
        self.temp -= cool_temp_decrease

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def neutron_hit(self):
        """This is where most of the magic happens, whenever we have a split atom we generate heat and with some P trigger hits in neighbours"""
        
        self.temp += neutron_hit_temp_increase
        
        for x in range(neutron_hit_size):
            for y in range(neutron_hit_size):
                for z in range(neutron_hit_size):
                    hit_p = neutron_hit_p[x][y][z]
                    # TODO: adjust hit_p according rod depth
                    if random.random() > hit_p:
                        # No hit
                        continue
                    if not self.reactor.layout[x][y]:
                        # Nothing to hit
                        continue
                    try:
                        self.reactor.layout[x][y].neutron_hit(z)
                    except:
                        # Skip errors
                        pass

        pass

if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
