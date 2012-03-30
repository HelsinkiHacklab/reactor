#!/usr/bin/env python
import os,sys,math
import dbus
import dbus.service
import cell
import random
import reactor as reactor_module

default_max_speed = 1.0
default_scram_speed = 2.0
default_water_flow = 0.5 # 1.0 being max
water_flow_cf = 2.0 # Cooling factor
stomp_temp_decrease = 50 # Drop temp of each cell by this when stomp if triggered
steam_pressure_exponent = 3.5

class rod(dbus.service.Object):
    def __init__(self, bus, mainloop, path_base, x, y, depth, reactor):
        self.object_path = "%s/rod/%d/%d" % (path_base, x, y)
        self.bus_name = dbus.service.BusName('fi.hacklab.reactorsimulator.engine', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)

        self.loop = mainloop
        self.reactor = reactor
        self.x = x
        self.y = y
        self.well_depth = depth
        self.set_depth(float(depth)*random.uniform(0, 1)) # This is float so we can keep track of progress in smaller steps, for simulation purposes it will be rounded to int
        #self.set_depth(-2) # all-out
        self.current_max_speed = default_max_speed
        self.current_max_flow = 1.0
        self.current_water_flow = default_water_flow
        self.current_velocity = random.uniform(-1, 1) # Rod movement.  Expressed in layers per second. Initialize to random speed

        self.water_level = 1.0 # This is basically percentage of the full depth 1.0 means full of water
        self.steam_pressure = 0.0 # In whatever unit we feel is most convinient
        self.avg_temp = 0.0
        
        
        self.cells = []
        for i in range(self.well_depth):
            self.cells.append(cell.cell(bus, self.loop, self.object_path, self.x, self.y, i, self.reactor, self))

        # Final debug statement
        print "%s initialized" % self.object_path

    def tick(self, duration_seconds):
        # Update rod pos
        if (self.current_velocity != 0):
            d = self.depth + self.current_velocity * duration_seconds
            self.set_depth(d)

        # Simulate
        self.cool()
        self.decay()
        for cell in self.cells:
            cell.calc_blend_temp()
        self.calc_avg_temp()
        self.calc_steam_pressure()


    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def cell_melted(self):
        """Cell has melted, everything is AFU"""
        self.current_max_flow = 0.0
        self.current_water_flow = 0.0
        self.current_velocity = 0.0
        self.current_max_speed  = 0.0

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def stomp(self):
        """Decreases avg temperature by dropping temp in each cell temp by the set amount and recalculating"""
        for cell in self.cells:
            cell.temp -= stomp_temp_decrease
        self.calc_avg_temp()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def calc_steam_pressure(self):
        """Recalculates the value of the steam_pressure property and returns it"""
        self.steam_pressure = ((self.avg_temp + 273) ** steam_pressure_exponent) / ((100+273) ** steam_pressure_exponent)
        return self.steam_pressure

    def get_cell_temps(self):
        """Return list of cell temperatures"""
        return map(lambda x: x.temp, self.cells)

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def set_depth(self, depth):
        # Clamp range
        if depth < reactor_module.rod_min_depth: depth = reactor_module.rod_min_depth
        if depth > reactor_module.rod_max_depth: depth = reactor_module.rod_max_depth

        # Update depth values
        self.depth = float(depth)
        self.moderator_depth = math.floor(self.depth)
        self.tip_depth = self.moderator_depth+1

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def calc_avg_temp(self):
        """Recalculates the value of the avg_temp property and returns it"""
        self.avg_temp = sum(self.get_cell_temps()) / self.well_depth
        return self.avg_temp;

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def neutron_hit(self, depth):
        """Trigger neutron hit on cell at depth, indices start from zero"""
        self.cells[depth].neutron_hit()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def decay(self):
        """This is the time-based decay, it will be called by a timer in the reactor"""
        for cell in self.cells:
            cell.decay()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def cool(self):
        """This is the time-based cooling, it will be called by a timer in the reactor"""
        cool_by = self.current_water_flow * water_flow_cf
        for cell in self.cells:
            cell.cool(cool_by)

    def get_cell_neutrons(self):
        """Return list of cell neutrons_seen"""
        return map(lambda x: x.neutrons_seen, self.cells)

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def report(self):
        self.emit_temp(self.x, self.y, self.get_cell_temps(), self.object_path)
        self.emit_neutrons(self.x, self.y, self.get_cell_neutrons(), self.object_path)
        self.emit_pressure(self.x, self.y, self.steam_pressure, self.object_path)
        
        # TODO: Report dpeth and velocity
        self.emit_depth(self.x, self.y, self.depth, self.current_velocity, self.object_path)

        # Clear the neutron counts
        for cell in self.cells:
            cell.neutrons_seen = 0


        # Check the limits
        self.check_cell_melt()

    def check_cell_melt(self):
        """Checks if any cell has melted"""
        for cell_instance in self.cells:
            if cell_instance.temp < cell.cell_melt_temp:
                continue
            self.emit_cell_melted(self.x, self.y, cell_instance.depth, self.object_path)
            self.cell_melted()
            return
        return

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_cell_melted(self, x, y, z, sender):
        """Emitted when a cell in a rod melts"""
        if self.cells[z].melted:
            return
        self.cells[z].melted =  True
        print "Cell %d,%d,%d melted!" % (x,y,z)
        pass

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def calc_blend_temp(self):
        for cell in self.cells:
            cell.calc_blend_temp()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def sync_blend_temp(self):
        for cell in self.cells:
            cell.sync_blend_temp()
        self.calc_avg_temp()

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_depth(self, x, y, depth, velocity, sender):
        """This emits the current depth and velocity (<0 is going up >0 going down)"""
        pass

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_temp(self, x, y, temp, sender):
        """This emits the temperatures of the cells of the current rod"""
        pass

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_neutrons(self, x, y, neutrons, sender):
        """This emits the neutron counts of the cells of the current rod"""
        pass

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_pressure(self, x, y, pressure, sender):
        """This emits the pressure of current rod"""
        pass


if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
