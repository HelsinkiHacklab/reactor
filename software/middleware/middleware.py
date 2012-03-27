import os,sys,time
import dbus
import dbus.service



# TODO move to config (but yml might not allow such nice formatting
rod_map = [['  ', '  ', ' 1', ' 2', ' 3', '  ', '  '],
           ['  ', ' 4', ' #', ' 5', ' 6', ' 7', '  '],
           [' 8', ' 9', '10', '11', '12', ' #', '13'],
           ['14', '15', '16', '16', '18', '19', '20'],
           ['21', ' #', '22', '23', '24', '25', '26'],
           ['  ', '27', '28', '29', ' #', '30', '  '],
           ['  ', '  ', '31', '32', '33', '  ', '  ']] 


class ardubus_bridge(dbus.service.Object):
    def __init__(self, bus, loop, config):
        self.config = config
        self.bus = bus
        self.loop = loop

        self.object_path = '/fi/hacklab/reactorsimulator/middleware/bridge'
        self.bus_name = dbus.service.BusName('fi.hacklab.reactormiddleware', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)

        self.load_nm()
        self.load_servos()

        self.bus.add_signal_receiver(self.red_alert, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert")
        self.bus.add_signal_receiver(self.red_alert_reset, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert_reset")
        self.red_alert_active = False

        self.bus.add_signal_receiver(self.blowout, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_blowout")

        self.bus.add_signal_receiver(self.depth_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_depth")
        

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
        self.ardu_rodservos = self.bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino0')
    	self.set_rod_servo = self.ardu_rodservos.get_dbus_method('set_servo', 'fi.hacklab.ardubus')



