import os,sys,time
import dbus
import dbus.service

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


class ardubus_bridge(dbus.service.Object):
    def __init__(self, bus, loop, config):
        self.config = config
        self.bus = bus
        self.loop = loop

        self.object_path = '/fi/hacklab/reactorsimulator/middleware/bridge'
        self.bus_name = dbus.service.BusName('fi.hacklab.reactorsimulator.middleware', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)

        self.load_nm()
        self.load_servos()

        self.bus.add_signal_receiver(self.red_alert, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert")
        self.bus.add_signal_receiver(self.red_alert_reset, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert_reset")
        self.red_alert_active = False

        self.bus.add_signal_receiver(self.blowout, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_blowout")

        self.bus.add_signal_receiver(self.depth_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_depth")

        self.max_neutrons_seen = 0
        # Listen temp/neutrons only from the measurment wells
        self.bus.add_signal_receiver(self.neutron_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_neutrons", path='/fi/hacklab/reactorsimulator/engine/reactor/mwell')
        #self.bus.add_signal_receiver(self.temp_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_temp", path='/fi/hacklab/reactorsimulator/engine/reactor/mwell')
        


    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def led_gauge(self, start_led, num_leds, value, map_max):
        jbol_idx = 0
        # interpolate
        mapped_value = int(np.interp(value, [0,map_max],[0,num_leds*255]))
        # and bin to leds
        for i in range(num_leds):
            ledno = start_led + 2*i
            if mapped_value > 255:
                self.set_rod_leds(jbol_idx, ledno, 255)
                mapped_value -= 255
                continue
            self.set_rod_leds(jbol_idx, ledno, mapped_value)
            break

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
        self.set_rod_servo(rod_id, int((255.0/7)*depth))

    def load_nm(self):
        self.nm = self.bus.get_object('fi.hacklab.noisemaker', '/fi/hacklab/noisemaker/noisemaker0')

    def load_servos(self):
        if not self.ardu_rodservos:
            self.ardu_rodservos = self.bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino0')
    	self.set_rod_servo = self.ardu_rodservos.get_dbus_method('set_servo', 'fi.hacklab.ardubus')

    def load_leds(self):
        if not self.ardu_rodservos:
            self.ardu_rodservos = self.bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino0')
    	self.set_rod_leds = self.ardu_rodservos.get_dbus_method('set_jbol_pwm', 'fi.hacklab.ardubus')

    def neutron_report(self, x, y, neutrons, *args):
        # Autoscale at least until we know what the scales are
        current_max = max(neutrons)
        if current_max > self.max_neutrons_seen:
            self.max_neutrons_seen = current_max
        led_base_index = (gauges8leds_map[x][y]*16)+8
        neutron_avg = sum(neutrons)/len(neutrons)
        self.led_gauge(led_base_index, 4, neutron_avg, self.max_neutrons_seen)

    def temp_report(self, x, y, temps, *args):
        led_base_index = (gauges8leds_map[x][y]*16)
        temp_avg = sum(temps)/len(temps)
        self.led_gauge(led_base_index, 4, temp_avg, self.max_temp)


