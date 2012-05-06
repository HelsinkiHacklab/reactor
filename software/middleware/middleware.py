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
import thread
import re

rodcontrol_regex = re.compile("rod_(\d)_(\d)_(down|up)")


# TODO move to config (but yml might not allow such nice formatting
gauges8leds_map = [[' ', ' ', '*', '*', '*', ' ', ' '],
                   [' ', '*', '0', '*', '*', '*', ' '],
                   ['*', '*', '*', '*', '*', '1', '*'],
                   ['*', '*', '*', '*', '*', '*', '*'],
                   ['*', '2', '*', '*', '*', '*', '*'],
                   [' ', '*', '*', '*', '3', '*', ' '],
                   [' ', ' ', '*', '*', '*', ' ', ' ']] 


max_temp = 800

measurement_well_coords = [(1,2),(2,5),(4,1),(5,4)]

reactor_square_side = 7

class middleware(service.baseclass):
    def __init__(self, config, launcher_instance, **kwargs):
        super(middleware, self).__init__(config, launcher_instance, **kwargs)
        self.config_reloaded()

        self.load_nm()

        # TODO: Read the board names from config
#        self.bus.add_signal_receiver(self.stomp_received, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_change", path="/fi/hacklab/ardubus/arduino2")
#        self.bus.add_signal_receiver(self.rod_switch_change, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_change", path="/fi/hacklab/ardubus/arduino1")

        self.bus.add_signal_receiver(self.aliased_signal_received, dbus_interface = "fi.hacklab.ardubus", signal_name = "alias_change", )

        self.bus.add_signal_receiver(self.red_alert, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert")
        self.bus.add_signal_receiver(self.red_alert_reset, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert_reset")
        self.red_alert_active = False

        self.bus.add_signal_receiver(self.blowout, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_blowout")

        # This seems to make us a bit slow (probably because now we do not cache the object...)
        self.bus.add_signal_receiver(self.depth_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_depth")

        self.max_neutrons_seen = 0

        self.dbus_cache = {}
        self.dbus_cache_error_count = {}
        
        # Listen temp/neutrons only from the measurment wells (filtering done on the receiver end it seems we could not do wildcard path matching afterall [maybe I should rethink these interface spaces])
        # Enumerate the well paths to limit the torrent of signals we need to process
        for coords in measurement_well_coords:
            well_busname = "fi.hacklab.reactorsimulator.engine.reactor.mwell.x%d.y%d" % coords
            well_path = "/fi/hacklab/reactorsimulator/engine/reactor/mwell/%d/%d" % coords
            self.bus.add_signal_receiver(self.neutron_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_neutrons", path=well_path)
            self.bus.add_signal_receiver(self.temp_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_temp", path=well_path)



    def config_reloaded(self):
        # Transpose the rod servo map to something more usable
        self.servo_position_cache = {}
        self.rod_servo_map = [[None for i in range(reactor_square_side)] for i in  range(reactor_square_side)]
        for board in self.config['rod_servo_map'].keys():
            for servo_idx in self.config['rod_servo_map'][board].keys():
                rodx,rody = self.config['rod_servo_map'][board][servo_idx]
                self.rod_servo_map[rodx][rody] = (servo_idx, board)


    def aliased_signal_received(self, alias, state, sender):
        rodcontrol_match = rodcontrol_regex.match(alias)
        if rodcontrol_match:
            coords = (rodcontrol_match.group(1), rodcontrol_match.group(2))
            rod_busname = "fi.hacklab.reactorsimulator.engine.reactor.rod.x%d.y%d" % coords
            rod_path = "/fi/hacklab/reactorsimulator/engine/reactor/rod/%d/%d" % coords
            if state: # high means switched off due to pull-ups
                return self.call_cached(rod_busname, rod_path, 'stop_move')
            direction = rodcontrol_match.group(3)
            if direction == 'up':
                return self.call_cached(rod_busname, rod_path, 'start_move', True)
            # The other possible match for the regex is "down"
            return self.call_cached(rod_busname, rod_path, 'start_move', False)


    def rod_switch_change(self, pin, state, sender, *args):
        print "Pin %d changed to %s on %s" % (pin, repr(state), sender)

        # TODO: Read the board names from config
        try:
            rod_info = self.config['rod_control_map']['arduino1'][int(pin)]
        except KeyError:
            print "No rod defined for pin %d" % pin
            return
        
        if bool(state):
            # High means pulled up, ie not switched
            self.call_cached('fi.hacklab.reactorsimulator.engine', "/fi/hacklab/reactorsimulator/engine/reactor/rod/%d/%d" % (rod_info[0],rod_info[1]), 'stop_move')
            return
        self.call_cached('fi.hacklab.reactorsimulator.engine', "/fi/hacklab/reactorsimulator/engine/reactor/rod/%d/%d" % (rod_info[0],rod_info[1]), 'start_move', rod_info[2])

    def call_cached(self, busname, buspath, method, *args):
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
        # Seems we fats run out of threads...
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

# OLD code for reference
#    @dbus.service.method('fi.hacklab.reactorsimulator.middleware')
#    def led_gauge(self, start_led, num_leds, value, map_max):
#        jbol_idx = 0
#        # interpolate (TODO: Is numpy fast here ?)
#        mapped_value = int(np.interp(value, [0,map_max],[0,num_leds*255]))
#        # and bin to leds
#        for i in range(num_leds):
#            #print "i=%d, mapped_value=%d" % (i, mapped_value)
#            ledno = start_led + 2*(num_leds-1) - 2*i
#            if mapped_value > 255:
#                #print "self.set_rod_leds(%d, %d, 255)" % (jbol_idx, ledno)
#                #self.bus.get_object('fi.hacklab.ardubus.arduino1', '/fi/hacklab/ardubus/arduino1').set_jbol_pwm(dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(255))
#                self.call_cached('fi.hacklab.ardubus.arduino1', '/fi/hacklab/ardubus/arduino1', 'set_jbol_pwm', dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(255))
#                mapped_value -= 255
#                continue
#            if mapped_value < 0:
#                #print "self.set_rod_leds(%d, %d, 0)" % (jbol_idx, ledno)
#                #self.bus.get_object('fi.hacklab.ardubus.arduino1', '/fi/hacklab/ardubus/arduino1').set_jbol_pwm(dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(0))
#                self.call_cached('fi.hacklab.ardubus.arduino1', '/fi/hacklab/ardubus/arduino1', 'set_jbol_pwm', dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(0))
#                continue
#            #print "self.set_rod_leds(%d, %d, %d)" % (jbol_idx, ledno, mapped_value)
#            #self.bus.get_object('fi.hacklab.ardubus.arduino1', '/fi/hacklab/ardubus/arduino1').set_jbol_pwm(dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(mapped_value))
#            self.call_cached('fi.hacklab.ardubus.arduino1', '/fi/hacklab/ardubus/arduino1', 'set_jbol_pwm', dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(mapped_value))
#            mapped_value -= 255

    def led_gauge(self, gauge_id, value, map_max):
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

    def red_alert(self, *args):
        if self.red_alert_active:
            return
        self.red_alert_active = True
        # TODO: make these configurable
        self.nm.play_sample('alarm.wav')

    def red_alert_reset(self, *args):
        self.red_alert_active = False
        # TODO: if the alert is loop remove it

    def blowout(self, *args):
        # TODO: make these configurable
        self.nm.play_sample('steam_release.wav')


    def load_nm(self):
        self.nm = self.bus.get_object('fi.hacklab.noisemaker', '/fi/hacklab/noisemaker')

    def neutron_report(self, x, y, neutrons, *args):
        x = int(x)
        y = int(y)
        if self.rod_servo_map[x][y] <> None:
            # This is an actual rod (the measurement wells have "None" here
            return
        if gauges8leds_map[x][y] == '*':
            print "somehow %d,%d was passed in as a well" % (x,y)
            return

        current_max = max(neutrons)
        if current_max > self.max_neutrons_seen:
            self.max_neutrons_seen = current_max
        neutron_avg = sum(neutrons)/len(neutrons)
        #led_base_index = (int(gauges8leds_map[x][y])*8)
        #self.led_gauge(led_base_index, 4, neutron_avg, self.config['neutron_gauge']['max_flux'])
        self.led_gauge("well_%d_%d_neutrons" % (x,y), neutron_avg, self.config['neutron_gauge']['max_flux'])

    def temp_report(self, x, y, temps, *args):
        x = int(x)
        y = int(y)
        if self.rod_servo_map[x][y] <> None:
            # This is an actual rod (the measurement wells have "None" here
            return
        if gauges8leds_map[x][y] == '*':
            print "somehow %d,%d was passed in as a well" % (x,y)
            return
        #print "temperatures for %d,%d,%s" % (x,y,temps)
        temp_avg = sum(temps)/len(temps)
        #led_base_index = (int(gauges8leds_map[x][y])*8)+1
        #self.led_gauge(led_base_index, 4, temp_avg, self.config['temp_gauge']['max_temp'])
        self.led_gauge("well_%d_%d_temp" % (x,y), temp_avg, self.config['temp_gauge']['max_temp'])



