# Boilerplate to add ../pythonlibs (via full path resolution) to import paths
import os,sys
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)

import dbus,gobject

import rod, measurementwell


###
# suovulan luettelemia lukuja
#
# cooling water normally 75 atm jolloin temp olis about 285C
# high-pressure jotain 158 atm
# 
#



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
max_temp = 1200.0 # This is used in visualizations etc, the max point temperature we are going to see while the reactor has not yet blown up

# Size of reactor (outer bounds)
reactor_width = len(default_layout)
reactor_height = len(default_layout[0])
reactor_depth = default_depth
reactor_cube_size = reactor_width * reactor_height * reactor_depth


# Reactor rod labeling
numbering_base = 4
numbering_start = numbering_base
numbering_digits = 2

def cell_type(x, y):
    """ Type of the specified cell """
    return default_layout[y][x]

def cell_name(x, y):
    """ Label of the specified cell """
    return "" + cell_row_name(y) + "-" + cell_column_name(x)

def cell_column_name(x):
    """ Label of the specified column """
    return baseN(numbering_start + x, numbering_base).zfill(numbering_digits)

def cell_row_name(y):
    """ Label of the specified row """
    return baseN(numbering_start + reactor_height - y - 1, numbering_base).zfill(numbering_digits)

# Converts number to specified base, from the internets: http://stackoverflow.com/questions/2267362/convert-integer-to-a-string-in-a-given-numeric-base-in-python
def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])


# Rod range
rod_min_depth = -2
rod_max_depth = reactor_depth

class reactor(dbus.service.Object):
    def __init__(self, simulation_instance, path_base):
        self.simulation_instance = simulation_instance
        self.object_path = path_base + '/reactor'
        self.bus = self.simulation_instance.bus
        self.bus_name = dbus.service.BusName('fi.hacklab.reactorsimulator.engine.reactor', bus=self.bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)

        global max_temp # Other modules might use this so if we get a new value from config try to override this
        self.config = self.simulation_instance.config['reactor']
        max_temp = self.config['max_temp']


        self.tick_count = 0
        self.grid_limits = [0,0,0]

        self.avg_temp = 0.0
        self.avg_pressure = 0.0
        self.max_temp = 0.0
        self.max_pressure = 0.0
        self.power_output = 0.0

        self.red_alert_given = False

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
                    col.append(rod.rod(self, x, y, depth))
                    self.rods.append(col[y])
                    continue
                if (layout[x][y] == '#'):
                    col.append(measurementwell.well(self, x, y, depth))
                    self.mwells.append(col[y])
                    continue
                # Default case is to skip
                col.append(None)
            self.layout.append(col)
        self.rod_count = len(self.rods)

    def unload(self):
        for rod_i in self.rods:
            rod_i.unload()
        del(rod_i)
        for i in range(len(self.rods)-1):
            del(self.rods[0])

        for mwell_i in self.mwells:
            mwell_i.unload()
        del(mwell_i)
        for i in range(len(self.mwells)-1):
            del(self.mwells[0])
        
        self.remove_from_connection()


    def config_reloaded(self):
        global max_temp # Other modules might use this so if we get a new value from config try to override this
        self.config = self.simulation_instance.config['reactor']
        max_temp = self.config['max_temp']

        for i in range(len(self.rods)-1):
            self.rods[i].config_reloaded()

        for i in range(len(self.mwells)-1):
            self.mwells[i].config_reloaded()

    def tick(self, duration_seconds):
        self.tick_count += 1

        # Call the decay methods on the rods
        for rod in self.rods:
            rod.tick(duration_seconds) # This method will update rod avg temp
        
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
        self.calc_max_temp()
        self.calc_max_pressure()

        # Trigger reports at each tick
        self.report()

        #print "Reactor tick #%d done" % self.tick_count

        # return true to keep ticking
        return True


    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def scram(self):
        """Slams all rods down as fast as they will go"""
        print "SCRAM!"
        for rod in self.rods:
            rod.scram()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def turbo(self):
        """Moves all control rods up, fun to play with"""
        for rod in self.rods:
            rod.start_move(True)

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def report(self):
        """This will trigger report methods for everything else, they will emit signals"""

        for rod in self.rods:
            rod.report()

        for well in self.mwells:
            well.report()

        self.emit_avg_pressure(self.avg_pressure, self.object_path)
        self.emit_avg_temperature(self.avg_temp, self.object_path)
        self.emit_max_pressure(self.max_pressure, self.object_path)
        self.emit_max_temperature(self.max_temp, self.object_path)
        self.emit_power(self.power_output, self.object_path)

        # Check limits
        self.check_pressure()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def check_pressure(self):
        if (self.avg_pressure > (self.config['blowout_pressure'] * self.config['blowout_safety_factor'])):
            self.emit_redalert(self.object_path)

        if self.avg_pressure > self.config['blowout_pressure']:
            self.emit_blowout(self.object_path)
            self.simulation_instance.pause()
        
        if (self.avg_pressure < (self.config['blowout_pressure'] * self.config['blowout_safety_factor'])):
            if self.red_alert_given:
                self.emit_redalert_reset(self.object_path)
        
    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_redalert_reset(self, sender):
        """Reset the alarm"""
        self.red_alert_given = False
        print "Red alert reset"

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_redalert(self, sender):
        """Sound the alarm!"""
        if self.red_alert_given:
            return
        self.red_alert_given = True
        print "RED ALERT!!!"

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_blowout(self, sender):
        """It's all over"""
        print "FAIL: Reactor blew up!"

    def get_rod_temps(self):
        """Return list of rod temperatures, NOTE: does not trigger recalculation on the rod so might return old data"""
        return map(lambda x: x.avg_temp, self.rods)

    def get_rod_max_temps(self):
        """Return list of rod maximum temperatures, NOTE: does not trigger recalculation on the rod so might return old data"""
        return map(lambda x: x.max_temp, self.rods)

    def get_rod_pressures(self):
        """Return list of rod pressures, NOTE: does not trigger recalculation on the rod so might return old data"""
        return map(lambda x: x.steam_pressure, self.rods)

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def calc_avg_temp(self):
        """Recalculates the value of the avg_temp property and returns it"""
        self.avg_temp = sum(self.get_rod_temps()) / self.rod_count
        return self.avg_temp

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def calc_avg_pressure(self):
        """Recalculates the value of the avg_pressure property and returns it, also recalculates power output"""
        self.avg_pressure = sum(self.get_rod_pressures()) / self.rod_count
        if self.avg_pressure > 1.0:
            self.power_output = self.avg_pressure * self.config['power_output_factor']
        else:
            self.power_output = 0.0
        return self.avg_pressure

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def calc_max_temp(self):
        """Recalculates the value of the max_temp property and returns it"""
        self.max_temp = max(self.get_rod_max_temps())
        return self.max_temp

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def calc_max_pressure(self):
        """Recalculates the value of the max_pressure property and returns it"""
        self.max_pressure = max(self.get_rod_pressures())
        return self.max_pressure

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_avg_pressure(self, pressure, sender):
        """This emits the average pressure """
        pass

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_avg_temperature(self, temperature, sender):
        """This emits the average temperature"""
        pass

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_max_pressure(self, pressure, sender):
        """This emits the maximum pressure in any rod channel"""
        pass

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_max_temperature(self, temperature, sender):
        """This emits the maximum temperature in any cell"""
        pass

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_power(self, power, sender):
        """This emits the average pressure """
        pass


if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
