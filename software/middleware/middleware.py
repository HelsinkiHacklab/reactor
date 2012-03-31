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
rod_map = [['  ', '  ', ' 1', ' 2', ' 3', '  ', '  '],
           ['  ', ' 4', ' #', ' 5', ' 6', ' 7', '  '],
           [' 8', ' 9', '10', '11', '12', ' #', '13'],
           ['14', '15', '16', '16', '18', '19', '20'],
           ['21', ' #', '22', '23', '24', '25', '26'],
           ['  ', '27', '28', '29', ' #', '30', '  '],
           ['  ', '  ', '31', '32', '33', '  ', '  ']] 

gauges8leds_map = [[' ', ' ', '*', '*', '*', ' ', ' '],
                  [' ', '*', '0', '*', '*', '*', ' '],
                  ['*', '*', '*', '*', '*', '1', '*'],
                  ['*', '*', '*', '*', '*', '*', '*'],
                  ['*', '2', '*', '*', '*', '*', '*'],
                  [' ', '*', '*', '*', '3', '*', ' '],
                  [' ', ' ', '*', '*', '*', ' ', ' ']] 


max_temp = 800


class middleware(service.baseclass):
    def __init__(self, config, launcher_instance, **kwargs):
        super(middleware, self).__init__(config, launcher_instance, **kwargs)


        self.load_nm()
        self.ardu_rodservos = None
        self.ardu_rodleds = None
        self.load_servos()
        self.load_leds()

        self.bus.add_signal_receiver(self.red_alert, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert")
        self.bus.add_signal_receiver(self.red_alert_reset, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert_reset")
        self.red_alert_active = False

        self.bus.add_signal_receiver(self.blowout, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_blowout")

        self.bus.add_signal_receiver(self.depth_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_depth")

        self.max_neutrons_seen = 0
        # Listen temp/neutrons only from the measurment wells
        #self.bus.add_signal_receiver(self.neutron_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_neutrons")
        #self.bus.add_signal_receiver(self.temp_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_temp",)
        
        #self.bus.add_signal_receiver(self.temp_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_temp",)

        self.bus.add_signal_receiver(self.stomp_received, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_change", path="/fi/hacklab/ardubus/arduino2")

    def stomp_received(self, pin, state, sender, *args):
        print "Pin %d changed(index) to %s on %s" % (pin, state, sender)
        if state:
            # high means pulled up, ie not switched
            return
        rod_y,rod_x = self.config['stomp_map']['pins2rods'][pin]
        print "Stomped on rod %d,%d" % (rod_y,rod_x)
        rod = self.bus.get_object('fi.hacklab.reactorsimulator.engine', "/fi/hacklab/reactorsimulator/engine/reactor/rod/%d/%d" % (rod_y,rod_x))
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
                self.set_rod_leds(jbol_idx, ledno, 255)
                mapped_value -= 255
                continue
            if mapped_value < 0:
                print "self.set_rod_leds(%d, %d, 0)" % (jbol_idx, ledno)
                self.set_rod_leds(jbol_idx, ledno, 0)
                continue
            print "self.set_rod_leds(%d, %d, %d)" % (jbol_idx, ledno, mapped_value)
            self.set_rod_leds(jbol_idx, ledno, mapped_value)
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

    def depth_report(self, x, y, depth, *args):
        rod_id = int(rod_map[x][y]) -1 # forgot to start from zero
        self.set_rod_servo(rod_id, int((255.0/9)*(depth+2)))

    def load_nm(self):
        self.nm = self.bus.get_object('fi.hacklab.noisemaker', '/fi/hacklab/noisemaker')

    def load_servos(self):
        if not self.ardu_rodservos:
            self.ardu_rodservos = self.bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino0')
    	self.set_rod_servo = self.ardu_rodservos.get_dbus_method('set_servo', 'fi.hacklab.ardubus')

    def load_leds(self):
        if not self.ardu_rodleds:
            self.ardu_rodleds = self.bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino1')
    	self.set_rod_leds = self.ardu_rodleds.get_dbus_method('set_jbol_pwm', 'fi.hacklab.ardubus')

    def neutron_report(self, x, y, neutrons, *args):
        #print "neutron check %s" % rod_map[x][y]
        if (rod_map[x][y] <> '#'):
            return
        # Autoscale at least until we know what the scales are
        print "neutrons for %d,%d,%s" % (x,y,neutrons)
        current_max = max(neutrons)
        if current_max > self.max_neutrons_seen:
            self.max_neutrons_seen = current_max
        led_base_index = (int(gauges8leds_map[x][y])*8)+4
        neutron_avg = sum(neutrons)/len(neutrons)
        self.led_gauge(led_base_index, 4, neutron_avg, self.max_neutrons_seen)

    def temp_report(self, x, y, temps, *args):
        #print "temp check %s" % rod_map[x][y]
        if (rod_map[x][y] <> '#'):
            return
        print "temperatures for %d,%d,%s" % (x,y,neutrons)
        led_base_index = (int(gauges8leds_map[x][y])*8)
        temp_avg = sum(temps)/len(temps)
        self.led_gauge(led_base_index, 4, temp_avg, self.max_temp)


