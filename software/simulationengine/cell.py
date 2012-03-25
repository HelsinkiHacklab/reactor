#!/usr/bin/env python
import os,sys,random
import dbus
import dbus.service

# Tuning parameters
neutron_hit_temp_increase = 0.5
cool_temp_decrease = 0.1
tip_neutron_hit_p_increase = 0.1
ambient_temp = 22.0
decay_p = 0.5 # P of causing neutron_hit when decay is called

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
        
        self.temp = ambient_temp # Celcius ?

        # Final debug statement
        print "%s initialized" % self.object_path

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def decay(self):
        """This is the time-based decay, it will be called by a timer in the reactor"""
        # Rod position is checked in the neutron_hit method
        if random.random() > decay_p:
            return
        self.neutron_hit()

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def cool(self):
        """This is the time-based cooling, it will be called by a timer in the reactor"""
        self.temp -= cool_temp_decrease
        if self.temp < ambient_temp:
            self.temp = ambient_temp
        print "DEBUG: %s cool(), temp %f" % (self.object_path, self.temp)


    @dbus.service.method('fi.hacklab.reactorsimulator')
    def neutron_hit(self):
        """This is where most of the magic happens, whenever we have a split atom we generate heat and with some P trigger hits in neighbours"""

        # If the moderator is past this point it will always absorb the hits, nothing will happen
        if (self.rod.moderator_depth >= self.depth):
            return
        
        self.temp += neutron_hit_temp_increase

        print "DEBUG: %s neutron_hit(), temp %f" % (self.object_path, self.temp)

        for x in range(neutron_hit_size):
            for y in range(neutron_hit_size):
                for z in range(neutron_hit_size):
                    hit_p = neutron_hit_p[x][y][z]
                    # The graphite tip is at our place, accelerate reaction
                    if (self.rod.tip_depth == z):
                        hit_p += tip_neutron_hit_p_increase
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
