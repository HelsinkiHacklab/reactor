#!/usr/bin/env python
import os,sys,time
try:
    import cpickle as pickle
except ImportError:
    import pickle
import dbus
import dbus.service
import reactor
import gobject

save_every_n_ticks = 50

class state(dbus.service.Object):
    def __init__(self, bus, mainloop):
        # DBUS boilerplate
        self.object_path = '/fi/hacklab/reactorsimulator/engine'
        self.bus_name = dbus.service.BusName('fi.hacklab.reactorsimulator.engine', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)
        
        # Load the reactor object (that will load most of the other stuff)
        self.loop = mainloop
        self.reactor = reactor.reactor(bus, self.loop, self.object_path, self)
        self.reactor.load_layout(reactor.default_layout, reactor.default_depth)
        self.tick_count = 0

        # Final debug statement
        print "%s initialized" % self.object_path

    def tick(self):
        """Wrapper to reactors tick method to allow us to pause the simulation"""
        if not self.is_running:
            return False
        self.tick_count += 1
        if ((self.tick_count % save_every_n_ticks) == 1):
            self.save_state()
        return self.reactor.tick()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def run(self):
        self.is_running = True
        # Set the reactor to tick every 100ms
        gobject.timeout_add(200, self.tick)
        if not self.loop.is_running():
            self.loop.run()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def pause(self):
        """Just sets an internal variable to control ticks"""
        self.is_running = False

    def quit(self):
        self.is_running = False
        self.loop.quit()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def get_state(self):
        pass

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def save_state(self):
        pass
        
    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def load_state(self):
        pass


if __name__ == '__main__':
    print "Use simulationengine.py"
    sys.exit(1)
