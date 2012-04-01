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



# TODO move to config (but yml might not allow such nice formatting
gauges8leds_map = [[' ', ' ', '*', '*', '*', ' ', ' '],
                  [' ', '*', '0', '*', '*', '*', ' '],
                  ['*', '*', '*', '*', '*', '1', '*'],
                  ['*', '*', '*', '*', '*', '*', '*'],
                  ['*', '2', '*', '*', '*', '*', '*'],
                  [' ', '*', '*', '*', '3', '*', ' '],
                  [' ', ' ', '*', '*', '*', ' ', ' ']] 


max_temp = 800


reactor_square_side = 7

class middleware(service.baseclass):
    def __init__(self, config, launcher_instance, **kwargs):
        super(middleware, self).__init__(config, launcher_instance, **kwargs)
        self.config_reloaded()

        self.load_nm()

        self.bus.add_signal_receiver(self.red_alert, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert")
        self.bus.add_signal_receiver(self.red_alert_reset, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert_reset")
        self.red_alert_active = False

        self.bus.add_signal_receiver(self.blowout, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_blowout")

        #self.bus.add_signal_receiver(self.depth_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_depth")

        self.max_temp = 1200
        self.max_neutrons_seen = 0
        
        # Listen temp/neutrons only from the measurment wells (filtering done on the receiver end it seems we could not do wildcard path matching afterall [maybe I should rethink these interface spaces])
        #self.bus.add_signal_receiver(self.neutron_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_neutrons")
        #self.bus.add_signal_receiver(self.temp_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_temp",)
        
        #self.bus.add_signal_receiver(self.temp_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_temp",)

        self.bus.add_signal_receiver(self.stomp_received, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_change", path="/fi/hacklab/ardubus/arduino2")


    def config_reloaded(self):
        # Transpose the rod servo map to something more usable
        self.rod_servo_map = [[None for i in range(reactor_square_side)] for i in  range(reactor_square_side)]
        for board in self.config['rod_servo_map'].keys():
            for servo_idx in self.config['rod_servo_map'][board].keys():
                rodx,rody = self.config['rod_servo_map'][board][servo_idx]
                self.rod_servo_map[rodx][rody] = (servo_idx, board)


    def depth_report(self, x, y, depth, *args):
        servo_position = int(np.interp(float(depth), [-2,reactor_square_side],[0,180]))
        #print "depth report for rod %d,%d, depth is %.3f corresponding to servo position %d" % (x,y,depth, servo_position)
            
        servo_idx,board_name = self.rod_servo_map[int(x)][int(y)]
        
        # TODO: We should cache these objects while keeping calling conventions this simple (with automatic try/catch fallback for changed numeric id)
        self.bus.get_object('fi.hacklab.ardubus', "/fi/hacklab/ardubus/%s" % board_name).set_servo(dbus.Byte(servo_idx), dbus.Byte(servo_position))

    def stomp_received(self, pin, state, sender, *args):
        #print "Pin %d changed(index) to %s on %s" % (pin, repr(state), sender)
        if bool(state):
            # high means pulled up, ie not switched
            return
        rod_x,rod_y = self.config['stomp_map']['pins2rods'][pin]
        print "Stomped on rod %d,%d" % (rod_x,rod_y)

        # TODO: We should cache these objects while keeping calling conventions this simple (with automatic try/catch fallback for changed numeric id)
        rod = self.bus.get_object('fi.hacklab.reactorsimulator.engine', "/fi/hacklab/reactorsimulator/engine/reactor/rod/%d/%d" % (rod_x,rod_y))
        rod.stomp()

    @dbus.service.method('fi.hacklab.reactorsimulator.middleware')
    def quit(self):
        return self.launcher_instance.quit()

    @dbus.service.method('fi.hacklab.reactorsimulator.middleware')
    def reload(self):
        return self.launcher_instance.reload()

    @dbus.service.method('fi.hacklab.reactorsimulator.middleware')
    def led_gauge(self, start_led, num_leds, value, map_max):
        jbol_idx = 0
        # interpolate
        mapped_value = int(np.interp(value, [0,map_max],[0,num_leds*255]))
        # and bin to leds
        for i in range(num_leds):
            print "i=%d, mapped_value=%d" % (i, mapped_value)
            ledno = start_led + 2*i
            if mapped_value > 255:
                print "self.set_rod_leds(%d, %d, 255)" % (jbol_idx, ledno)
                # TODO: We should cache these objects while keeping calling conventions this simple (with automatic try/catch fallback for changed numeric id)
                self.bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino1').set_jbol_pwm(dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(255))
                mapped_value -= 255
                continue
            if mapped_value < 0:
                print "self.set_rod_leds(%d, %d, 0)" % (jbol_idx, ledno)
                # TODO: We should cache these objects while keeping calling conventions this simple (with automatic try/catch fallback for changed numeric id)
                self.bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino1').set_jbol_pwm(dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(0))
                continue
            print "self.set_rod_leds(%d, %d, %d)" % (jbol_idx, ledno, mapped_value)
            
            # TODO: We should cache these objects while keeping calling conventions this simple (with automatic try/catch fallback for changed numeric id)
            self.bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino1').set_jbol_pwm(dbus.Byte(jbol_idx), dbus.Byte(ledno), dbus.Byte(mapped_value))
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
        if self.rod_servo_map[int(x)][int(y)]:
            # This is an actual rod (the measurement wells have "None" here
            return

        # Autoscale at least until we know what the scales are
        print "neutrons for %d,%d,%s" % (x,y,neutrons)
        current_max = max(neutrons)
        if current_max > self.max_neutrons_seen:
            self.max_neutrons_seen = current_max
        led_base_index = (int(gauges8leds_map[x][y])*8)+1
        neutron_avg = sum(neutrons)/len(neutrons)
        self.led_gauge(led_base_index, 4, neutron_avg, self.max_neutrons_seen)

    def temp_report(self, x, y, temps, *args):
        if self.rod_servo_map[int(x)][int(y)]:
            # This is an actual rod (the measurement wells have "None" here
            return
        print "temperatures for %d,%d,%s" % (x,y,temps)
        led_base_index = (int(gauges8leds_map[x][y])*8)
        temp_avg = sum(temps)/len(temps)
        self.led_gauge(led_base_index, 4, temp_avg, self.max_temp)


