#!/usr/bin/env python
import os,sys
try:
    import cpickle as pickle
except ImportError:
    import pickle
import dbus
import dbus.service

class state(dbus.service.Object):
    def __init__(self, bus, mainloop):
        self.loop = mainloop
        self.object_path = '/fi/hacklab/reactorsimulator/simulationengine'
        self.bus_name = dbus.service.BusName('fi.hacklab.ardubus', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)

    def run(self):
        self.loop.run()

    def get_state(self):
        pass

    def save_state(self):
        pass
        
    def load_state(self):
        pass


if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
