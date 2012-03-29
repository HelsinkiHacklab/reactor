# Boilerplate to add ../pythonlibs (via full path resolution) to import paths
import os,sys
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)

# Import our DBUS service module
import service,dbus

# Import pickle for saving states
try:
    import cpickle as pickle
except ImportError:
    import pickle

# TODO: move to YAML config
save_every_n_ticks = 50

# Import the reactor module
import reactor

class simulation(service.baseclass):
    def __init__(self, mainloop, bus, config, **kwargs):
        super(simulation, self).__init__(mainloop, bus, config, **kwargs)

        self.reactor = reactor.reactor(bus, self.mainloop, self.dbus_object_path, self)
        self.reactor.load_layout(reactor.default_layout, reactor.default_depth)
        self.tick_count = 0
        self.run()

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

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def reset(self):
        """Resets the simulation to startinng conditions"""
        pass

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def pause(self):
        """Just sets an internal variable to control ticks"""
        self.is_running = False

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def save_state(self):
        pass
        
    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def load_state(self):
        pass

    def config_reloaded(self):
        # TODO: pass this info down to all the other instances
        pass
