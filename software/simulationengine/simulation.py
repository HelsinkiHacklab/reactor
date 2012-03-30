# Boilerplate to add ../pythonlibs (via full path resolution) to import paths
import os,sys
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)

# Import our DBUS service module
import service,dbus,gobject

# Import pickle for saving states
try:
    import cpickle as pickle
except ImportError:
    import pickle
import time

# TODO: move to YAML config
save_every_n_ticks = 50

# Import the reactor module
import reactor

class simulation(service.baseclass):
    def __init__(self, mainloop, bus, config, **kwargs):
        super(simulation, self).__init__(mainloop, bus, config, **kwargs)

        self.reactor = None
        self.reset()
        self.run()

    def tick(self):
        """Wrapper to reactors tick method to allow us to pause the simulation"""
        if not self.is_running:
            self.last_tick_time = 0
            return False
        else:
            # Save state regularly
            self.tick_count += 1
            if ((self.tick_count % save_every_n_ticks) == 1):
                self.save_state()

            # Calculate seconds since last tick
            now = time.time()
            duration_seconds = 0
            if self.last_tick_time != 0:
                duration_seconds = now - self.last_tick_time
            self.last_tick_time = now

            # Tick all subsystems
            return self.reactor.tick(duration_seconds)

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def run(self):
        print "RUNNING"
        self.is_running = True
        # Set the reactor to tick every N ms
        gobject.timeout_add(200, self.tick)

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def reset(self):
        """Resets the simulation to startinng conditions"""
        if self.reactor:
            self.reactor.unload()
            del(self.reactor)
        self.reactor = reactor.reactor(self, self.dbus_object_path)
        self.reactor.load_layout(reactor.default_layout, reactor.default_depth)
        self.tick_count = 0
        self.last_tick_time = 0

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def pause(self):
        """Just sets an internal variable to control ticks"""
        print "PAUSED"
        self.is_running = False

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def save_state(self):
        pass
        
    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def load_state(self):
        pass

    def config_reloaded(self):
        self.reactor.config_reloaded()
        pass
