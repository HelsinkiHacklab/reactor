import os,sys,time
import dbus
import dbus.service

class ardubus_bridge(dbus.service.Object):
    def __init__(self, bus, loop, config):
        self.config = config
        self.bus = bus
        self.loop = loop

        self.object_path = '/fi/hacklab/reactorsimulator/middleware/bridge'
        self.bus_name = dbus.service.BusName('fi.hacklab.reactormiddleware', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)

        self.load_nm()

        self.bus.add_signal_receiver(self.red_alert, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert")
        self.bus.add_signal_receiver(self.red_alert_reset, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_redalert_reset")
        self.red_alert_active = False


        self.bus.add_signal_receiver(self.blowout, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_blowout")
        

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
        self.nm = self.bus.get_object('fi.hacklab.noisemaker', '/fi/hacklab/noisemaker/noisemaker0')



