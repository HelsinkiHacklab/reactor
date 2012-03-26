#!/usr/bin/env python
import os,sys,random
import dbus, gobject
import dbus.service

# Tuning parameters
neutron_hit_temp_increase = 1.0
cool_temp_decrease = 0.1 # This is ambient radiative cooling, the rod will have active cooling that is defined there
tip_neutron_hit_p_increase = 0.1
ambient_temp = 22.0
decay_p = 0.5 # P of causing neutron_hit when decay is called
temperature_blend_weight = 0.1

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
        self.neutrons_seen = 0
        
        
        self.temp = float(ambient_temp) # Celcius ?
        self.blend_temp = 0.0

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
    def cool(self, cool_by=None):
        """This is the time-based cooling, it will be called by a timer in the reactor"""
        if not cool_by:
            self.temp -= cool_temp_decrease
        else:
            self.temp -= cool_by
        if self.temp < ambient_temp:
            self.temp = ambient_temp
        print "DEBUG: %s cool(), temp %f" % (self.object_path, self.temp)

    def calc_blend_temp(self):
        """Calculates next blend_temp"""
        self.blend_temp = 0.0
        cell_count = 0
        for xdelta in range(neutron_hit_size):
            for ydelta in range(neutron_hit_size):
                for zdelta in range(neutron_hit_size):
                    x = self.x + (xdelta - 1)
                    y = self.y + (ydelta - 1)
                    z = self.depth + (zdelta - 1)
                    if not self.reactor.in_grid(x,y,z):
                        #print "DEBUG blend [%d,%d,%d] is outside the grid" % (x,y,z)
                        continue
                    if not self.reactor.layout[x][y]:
                        #print "DEBUG blend [%d,%d] has no rod" % (x,y)
                        # Nothing there
                        continue
                    try:
                        n_temp = self.reactor.layout[x][y].cells[z].temp
                    except:
                        try:
                            n_temp = self.reactor.layout[x][y].temperatures[z] # blend the measurement wells too
                        except:
                            pass
                    self.blend_temp += n_temp # Sum neighbouring cell temps
                    cell_count += 1

        if not cell_count:
            self.blend_temp = self.temp
            return
        self.blend_temp /= cell_count # and average them
        self.blend_temp = (1.0 - temperature_blend_weight) * self.temp + (temperature_blend_weight * self.blend_temp)

    def sync_blend_temp(self):
        """sync the buffered blend_temps to cell real temp"""
        self.temp = float(self.blend_temp)
        #print "DEBUG: %s sync_blend_temp(), temp %f" % (self.object_path, self.temp)

    @dbus.service.method('fi.hacklab.reactorsimulator')
    def neutron_hit(self):
        """This is where most of the magic happens, whenever we have a split atom we generate heat and with some P trigger hits in neighbours"""
        self.neutrons_seen += 1 # keep track of the flow in case we need it

        # If the moderator is past this point it will always absorb the hits, nothing will happen
        if (self.rod.moderator_depth >= self.depth):
            return
        
        self.temp += neutron_hit_temp_increase

        #print "DEBUG: %s neutron_hit(), temp %f" % (self.object_path, self.temp)

        for xdelta in range(neutron_hit_size):
            for ydelta in range(neutron_hit_size):
                for zdelta in range(neutron_hit_size):
                    x = self.x + (xdelta - 1)
                    y = self.y + (ydelta - 1)
                    z = self.depth + (zdelta - 1)
                    if not self.reactor.in_grid(x,y,z):
                        continue
                    hit_p = neutron_hit_p[xdelta][ydelta][zdelta]
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
                        # I guess these should be marshalled through mainloops event system
                        #self.reactor.layout[x][y].neutron_hit(z)
                        gobject.idle_add(self.reactor.layout[x][y].neutron_hit, z)
                    except:
                        # Skip errors
                        pass

        pass

if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
