import os,sys,time
import dbus
import dbus.service

class ardubus_bridge(dbus.service.Object):
    def __init__(self, bus, loop):
        self.bus = bus
        self.loop = loop
        self.object_path = '/fi/hacklab/reactorsimulator/middleware/bridge'
        self.bus_name = dbus.service.BusName('fi.hacklab.reactormiddleware', bus=bus)
        self.bus = bus
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)


        #self.bus.add_signal_receiver(self.temp_report, dbus_interface = "fi.hacklab.reactorsimulator", signal_name = "emit_temp")



    def