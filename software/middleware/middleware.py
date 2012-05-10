from __future__ import with_statement
# Boilerplate to add ../pythonlibs (via full path resolution) to import paths
import os,sys
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)

# Import our DBUS service module
import service,dbus,gobject
import dbus,time

import numpy as np
import re

rodcontrol_regex = re.compile("rod_(\d)_(\d)_(down|up)")
rodstomp_regex = re.compile("rod_(\d)_(\d)_stomp")

# Define where the measurement wells are, used to limit amount of incoming signals
measurement_well_coords = [(1,2),(2,5),(4,1),(5,4)]

reactor_square_side = 7

class middleware(service.baseclass):
    def __init__(self, config, launcher_instance, **kwargs):
        super(middleware, self).__init__(config, launcher_instance, **kwargs)
        self.config_reloaded()

        # Simulation reset
        self.bus.add_signal_receiver(self.simulation_reset, dbus_interface = "fi.hacklab.reactorsimulator.engine", signal_name = "emit_simulation_reset")

        # Just about all signals we expect to get from the Arduinos will come in as aliased signals since those are so much more easier to map.
        self.bus.add_signal_receiver(self.aliased_signal_received, dbus_interface = "fi.hacklab.ardubus", signal_name = "alias_change")
        self.bus.add_signal_receiver(self.aliased_report_received, dbus_interface = "fi.hacklab.ardubus", signal_name = "alias_report")
        self.alias_state_cache = {}

        # Red-Alert state handling
        self.bus.add_signal_receiver(self.red_alert, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert")
        self.bus.add_signal_receiver(self.red_alert_reset, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert_reset")
        self.red_alert_active = False

        # Blowout signal
        self.bus.add_signal_receiver(self.blowout, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_blowout")

        # Rod depts, will be passed to the gauges
        self.bus.add_signal_receiver(self.depth_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_depth")


        # Cell warning signals
        self.bus.add_signal_receiver(self.cell_melt_warning, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_cell_melt_warning")
        self.bus.add_signal_receiver(self.cell_melt_warning_reset, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_cell_melt_warning_reset")
        self.bus.add_signal_receiver(self.cell_melted, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_cell_melted")
        self.active_melt_warnings = {} # keyed by sender (rod)
        

        # Used to keep track of the cached dbus proxy-objects
        self.dbus_cache = {}
        self.dbus_cache_error_count = {}
        
        # Listen temp/neutrons only from the measurment wells (filtering done on the receiver end it seems we could not do wildcard path matching afterall [maybe I should rethink these interface spaces])
        # Enumerate the well paths to limit the torrent of signals we need to process
        for coords in measurement_well_coords:
            well_busname = "fi.hacklab.reactorsimulator.engine.reactor.mwell.x%d.y%d" % coords
            well_path = "/fi/hacklab/reactorsimulator/engine/reactor/mwell/%d/%d" % coords
            self.bus.add_signal_receiver(self.neutron_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_neutrons", path=well_path)
            self.bus.add_signal_receiver(self.temp_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_temp", path=well_path)

        self.blink_states = {} 


    def config_reloaded(self):
        # Transpose the rod servo map to something more usable
        self.servo_position_cache = {}
        self.rod_servo_map = [[None for i in range(reactor_square_side)] for i in  range(reactor_square_side)]
        for board in self.config['rod_servo_map'].keys():
            for servo_idx in self.config['rod_servo_map'][board].keys():
                rodx,rody = self.config['rod_servo_map'][board][servo_idx]
                self.rod_servo_map[rodx][rody] = (servo_idx, board)


    def simulation_reset(self, sender):
        """Simulation has been reset, reset our state too"""
        # Remove all active loops
        loops = self.nm('list_loops')
        if loops:
            for loop_instance_name in loops:
                self.nm('stop_sequence', loop_instance_name)

        # TODO reset warning leds

        # Reset all simulation related state variables
        self.active_melt_warnings = {}
        self.red_alert_active = False

    def cell_melt_warning_reset(self, x, y, z, sender):
        if not self.active_melt_warnings.has_key(sender):
            return
        del(self.active_melt_warnings[sender])
        if len(self.active_melt_warnings) == 0:
            # No alarms left, remove the loop
            self.nm('stop_sequence', 'cell_melt_alarm0')

        # TODO: Remove blink-effect from the led corresponding to the rod

    @dbus.service.method('fi.hacklab.reactorsimulator.middleware')
    def start_blink(self, ledid, interval=750, maxpwm=255):
        self.blink_states[ledid] = { 'laststate': False, 'maxpwm': maxpwm, 'loop': True }
        gobject.timeout_add(interval, self.blink_loop, ledid)
        pass

    @dbus.service.method('fi.hacklab.reactorsimulator.middleware')
    def stop_blink(self, ledid):
        if not self.blink_states.has_key(ledid):
            return False
        # Rig the blinking to stop at next loop iteration
        self.blink_states[ledid]['laststate'] = True
        self.blink_states[ledid]['loop'] = False
        return True

    def blink_loop(self, ledid):
        if not self.blink_states.has_key(ledid):
            return False
        if self.blink_states[ledid]['laststate']:
            pwm = 0
            self.blink_states[ledid]['laststate'] = False
        else:
            pwm = self.blink_states[ledid]['maxpwm']
            self.blink_states[ledid]['laststate'] = True

        led_config = self.config['top_led_map']
        board_busname = 'fi.hacklab.ardubus.' + led_config['board']
        board_path = '/fi/hacklab/ardubus/' + led_config['board']
        jbol_idx = led_config['jbol_idx']
        ledno = led_config['led_ids'][ledid]

        self.call_cached(board_busname, board_path, 'set_jbol_pwm', dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(pwm))
        
        # Must return true to keep the timer ticking
        if self.blink_states[ledid]['loop']:
            return True
        else:
            del(self.blink_states[ledid])
            return False


    def cell_melt_warning(self, x, y, z, sender):
        if len(self.active_melt_warnings) == 0:
            # First cell melt warning, activate the loop
            self.nm('start_sequence', 'cell_melt_alarm', 'cell_melt_alarm0') # The latter is the loop instance identifier
             
        self.active_melt_warnings[sender] = True
        # TODO: Activate led effects
        pass

    def cell_melted(self, x, y, z, sender):
        if self.active_melt_warnings.has_key(sender):
            # First reset the warning
            self.cell_melt_warning_reset(x, y, z, sender)

        # Then go on to do whatever we do when a cell melts
        pass

    def aliased_report_received(self, alias, state, time, sender):
        """If we seem to have missed a state change signal trigger one based on the report (better late than never...)"""
        if (   not self.alias_state_cache.has_key(alias)
            or self.alias_state_cache[alias] != state):
            return self.aliased_signal_received(alias, state, sender)
        return

    def aliased_signal_received(self, alias, state, sender):
        """The main meat of the Arduino->simulation communication, aliased signals are matched using whatever rules and converted to commands passed on to the simulation"""
        # Update state cache
        self.alias_state_cache[alias] = state
        
        # Rod movement switches
        rodcontrol_match = rodcontrol_regex.match(alias)
        if rodcontrol_match:
            coords = (int(rodcontrol_match.group(1)), int(rodcontrol_match.group(2)))
            rod_busname = "fi.hacklab.reactorsimulator.engine.reactor.rod.x%d.y%d" % coords
            rod_path = "/fi/hacklab/reactorsimulator/engine/reactor/rod/%d/%d" % coords
            if state: # high means switched off due to pull-ups
                return self.call_cached(rod_busname, rod_path, 'stop_move')
            direction = rodcontrol_match.group(3)
            if direction == "up":
                return self.call_cached(rod_busname, rod_path, 'start_move', True)
            # The other possible match for the regex is "down"
            return self.call_cached(rod_busname, rod_path, 'start_move', False)

        # Simple and self-explained switches
        if alias == "SCRAM" and not state:
            return self.call_cached('fi.hacklab.reactorsimulator.engine.reactor', '/fi/hacklab/reactorsimulator/engine/reactor', 'scram')
        if alias == "TURBO" and not state:
            return self.call_cached('fi.hacklab.reactorsimulator.engine.reactor', '/fi/hacklab/reactorsimulator/engine/reactor', 'turbo')

        # Stomping switches
        rodstomp_match = rodstomp_regex.match(alias)
        if rodstomp_match and not state: # High is idle, active-low is the way we roll (mainly because the ATMega has internal pull-ups)
            coords = (int(rodstomp_match.group(1)), int(rodstomp_match.group(2)))
            rod_busname = "fi.hacklab.reactorsimulator.engine.reactor.rod.x%d.y%d" % coords
            rod_path = "/fi/hacklab/reactorsimulator/engine/reactor/rod/%d/%d" % coords
            return self.call_cached(rod_busname, rod_path, 'stomp')

    def call_cached(self, busname, buspath, method, *args):
        """Maintains a cache of DBUS proxy objects and calls the given objects method. If the proxy object is stale tries to refresh"""
        obj_cache_key = "%s@%s" % (busname, buspath)
        method_cache_key = "%s::%s" % (obj_cache_key, method)
        if not self.dbus_cache.has_key(obj_cache_key):
            self.dbus_cache[obj_cache_key] = self.bus.get_object(busname, buspath)
        if not self.dbus_cache.has_key(method_cache_key):
            self.dbus_cache[method_cache_key] = getattr(self.dbus_cache[obj_cache_key], method)

        try:
            ret = self.dbus_cache[method_cache_key](*args)
            if self.dbus_cache_error_count.has_key(method_cache_key): # Zero the error count
                self.dbus_cache_error_count[method_cache_key] = 0
            return ret                
        except dbus.exceptions.DBusException:
            if not self.dbus_cache_error_count.has_key(method_cache_key):
                self.dbus_cache_error_count[method_cache_key] = 0
            self.dbus_cache_error_count[method_cache_key] += 1
            # TODO Check that it's a method os object name exception first
            # Remove stale keys
            print "Removing stale keys for %s" % method_cache_key
            del(self.dbus_cache[obj_cache_key])
            del(self.dbus_cache[method_cache_key])
            if self.dbus_cache_error_count[method_cache_key] < 4:
                return self.call_cached(busname, buspath, method, *args)

    def depth_report(self, x, y, depth, *args):
        # Right now skip this
        return

        try:
            mapped = self.rod_servo_map[int(x)][int(y)]
        except KeyError:
            print "depth report for rod %d,%d, index out of range" % (x,y)
            return
        if not mapped:
            print "depth report for rod %d,%d, No rod defined there" % (x,y)
            # No rod there
            return
            
        servo_idx,board_name = mapped
        # interpolate (TODO: Is numpy fast here, at least it handles the negative depth correctly ?)
        servo_position = int(np.interp(float(depth), [-2,reactor_square_side],[0,180]))

        cache_key = "%s:%s" % (board_name, servo_idx)
        if not self.servo_position_cache.has_key(cache_key):
            self.servo_position_cache[cache_key] = -1

        if self.servo_position_cache[cache_key] == servo_position:
            # TODO: At some intervall refresh this anyway
            return

        # Can we background this call somehow ?
        self.call_cached('fi.hacklab.ardubus.' + board_name, '/fi/hacklab/ardubus/' + board_name, 'set_servo', dbus.Byte(servo_idx), dbus.Byte(servo_position))
        # Seems we fats run out of threads... (also those threads should probably have been .join():ed at some time, if this need arises looks at the multiprocessing module that has threadpools
        #thread.start_new_thread(self.call_cached, ('fi.hacklab.ardubus.' + board_name, '/fi/hacklab/ardubus/' + board_name, 'set_servo', dbus.Byte(servo_idx), dbus.Byte(servo_position)))

        self.servo_position_cache[cache_key] = servo_position

    def stomp_received(self, pin, state, sender, *args):
        print "Pin %d changed to %s on %s" % (pin, repr(state), sender)
        if bool(state):
            # high means pulled up, ie not switched
            return
        try:
            rod_x,rod_y = self.config['stomp_map']['pins2rods'][pin]
        except KeyError:
            print "No rod defined for pin %d" % pin
            return
        print "Stomped on rod %d,%d" % (rod_x,rod_y)

        self.call_cached('fi.hacklab.reactorsimulator.engine', "/fi/hacklab/reactorsimulator/engine/reactor/rod/%d/%d" % (rod_x,rod_y), 'stomp')

    @dbus.service.method('fi.hacklab.reactorsimulator.middleware')
    def quit(self):
        return self.launcher_instance.quit()

    @dbus.service.method('fi.hacklab.reactorsimulator.middleware')
    def reload(self):
        return self.launcher_instance.reload()

    @dbus.service.method('fi.hacklab.reactorsimulator.middleware')
    def led_gauge(self, gauge_id, value, map_max):
        """Renders a value mapped from 0 to map_max into led gauge of N leds (see config)"""
        gauge_config = self.config['led_gauge_map'][gauge_id]
        num_leds = len(gauge_config['leds'])
        board_busname = 'fi.hacklab.ardubus.' + gauge_config['board']
        board_path = '/fi/hacklab/ardubus/' + gauge_config['board']
        jbol_idx = gauge_config['jbol_idx']
        # Interpolate with numpy
        mapped_value = int(np.interp(value, [0,map_max],[0,num_leds*255]))
        # And bin to the leds
        for ledno in gauge_config['leds']:
            if mapped_value > 255:
                self.call_cached(board_busname, board_path, 'set_jbol_pwm', dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(255))
                mapped_value -= 255
                continue
            if mapped_value < 0:
                self.call_cached(board_busname, board_path, 'set_jbol_pwm', dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(0))
                continue
            self.call_cached(board_busname, board_path, 'set_jbol_pwm', dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(mapped_value))
            mapped_value -= 255

    def neutron_report(self, x, y, neutrons, *args):
        """Maintains the highest seen (average across the well) neutron flux and passes that and the current (average across the well) level to the led gauges"""
        x = int(x)
        y = int(y)
        neutron_avg = float(sum(neutrons))/float(len(neutrons))
        #print "neutron_report: neutron_avg=%f" % neutron_avg
#        if neutron_avg > self.max_neutron_avg:
#            self.max_neutron_avg = neutron_avg
#            print "neutron_report: self.max_neutron_avg updated to %f" % self.max_neutron_avg 
        self.led_gauge("well_%d_%d_neutrons" % (x,y), neutron_avg, self.config['neutron_gauge']['max_avgflux'])

    def temp_report(self, x, y, temps, *args):
        """Calculates the average temp of the well and passes that to the corresponding led-gauge, max level comes from config"""
        x = int(x)
        y = int(y)
        #print "temperatures for %d,%d,%s" % (x,y,temps)
        temp_avg = float(sum(temps))/float(len(temps))
        self.led_gauge("well_%d_%d_temp" % (x,y), temp_avg, self.config['temp_gauge']['max_temp'])

    def red_alert(self, *args):
        if self.red_alert_active:
            return
        self.red_alert_active = True
        self.nm('start_sequence', 'red_alert', 'red_alert0') # The latter is the loop instance identifier

    def red_alert_reset(self, *args):
        self.red_alert_active = False
        # TODO: if the alert is loop remove it (and use call_cached)
        self.nm('stop_sequence', 'red_alert0')

    def blowout(self, *args):
        # Cancel the other alarms
        self.nm('stop_sequence', 'cell_melt_alarm0')
        self.nm('stop_sequence', 'red_alert0')
        # TODO: make these configurable
        return self.play_sample('steam_release.wav')

    def play_sample(self, sample_name):
        """Simple sample player via noisemaker"""
        return self.call_cached('fi.hacklab.noisemaker', '/fi/hacklab/noisemaker', 'play_sample', sample_name)

    def nm(self, method, *args):
        """Passthrough to noisemaker via call_cached"""
        return self.call_cached('fi.hacklab.noisemaker', '/fi/hacklab/noisemaker', method, *args)
