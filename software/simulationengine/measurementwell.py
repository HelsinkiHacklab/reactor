#!/usr/bin/env python
import os,sys
import dbus
import dbus.service
import cell

class well(dbus.service.Object):
    def __init__(self, reactor, x, y, depth):
        self.reactor = reactor
        self.simulation_instance = self.reactor.simulation_instance
        self.object_path = "%s/mwell/%d/%d" % (self.reactor.object_path, x, y)
        self.bus_name = dbus.service.BusName('fi.hacklab.reactorsimulator.engine', bus=self.simulation_instance.bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)

        self.x = x
        self.y = y
        self.depth = depth
        
        self.neutrons_seen = [0 for i in range(self.depth)]
        self.temperatures = [0.0 for i in range(self.depth)]
        self.blend_temperatures = [0.0 for i in range(self.depth)]
        self.avg_temp = 0.0

        # Final debug statement
        print "%s initialized" % self.object_path

    def unload(self):
        pass

    def config_reloaded(self):
        pass

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def neutron_hit(self, depth):
        """Trigger neutron hit on cell at depth, indices start from zero"""
        self.neutrons_seen[depth] += 1 # keep track of the flow
        pass

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def calc_blend_temp(self):
        """Calculates next blend_temp"""
        self.blend_temperatures = [0.0 for i in range(self.depth)]
        for i in range(self.depth):
            cell_count = 0
            for xdelta in range(cell.neutron_hit_size):
                for ydelta in range(cell.neutron_hit_size):
                    for zdelta in range(cell.neutron_hit_size):
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
                        self.blend_temperatures[i] += n_temp # Sum neighbouring cell temps
                        cell_count += 1
        
            if not cell_count:
                self.blend_temperatures[i] = self.temperatures[i]
                continue
            self.blend_temperatures[i] /= cell_count # and average them
            self.blend_temperatures[i] = (1.0 - cell.temperature_blend_weight) * self.temperatures[i]  + (cell.temperature_blend_weight * self.blend_temperatures[i])
        pass

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def sync_blend_temp(self):
        for i in range(self.depth):
            self.temperatures[i] = float(self.blend_temperatures[i])
        self.calc_avg_temp()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def calc_avg_temp(self):
        """Recalculates the value of the avg_temp property and returns it"""
        self.avg_temp = sum(self.temperatures) / self.depth
        return self.avg_temp;

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def report(self):
        #self.emit_temp(self.temp, self.object_path)
        self.emit_neutrons(self.x, self.y, self.neutrons_seen, self.object_path)
        self.emit_temp(self.x, self.y, self.temperatures, self.object_path)
        self.neutrons_seen = [0 for i in range(self.depth)] # reset the count

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_neutrons(self, x, y, neutrons, sender):
        """This emits the temperature of current cell"""
        pass

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_temp(self, x, y, temp, sender):
        """This emits the temperatures of the cells of the current rod"""
        pass


if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
