import os,sys,time
import dbus
import dbus.service

class listener():
    def __init__(self, bus, loop):
        self.bus = bus
        self.loop = loop


        #self.bus.add_signal_receiver(self.temp_report, dbus_interface = "fi.hacklab.reactorsimulator", signal_name = "emit_temp")



