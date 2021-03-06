from __future__ import with_statement
# Boilerplate to add ../pythonlibs (via full path resolution) to import paths
import os,sys
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)

# Import our DBUS service module
import service,dbus,gobject

import time

# Import the reactor module
import reactor

class simulation(service.baseclass):
    def __init__(self, config, launcher_instance, **kwargs):
        super(simulation, self).__init__(config, launcher_instance, **kwargs)

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
            #if ((self.tick_count % self.config['simulation']['autosave_interval']) == 1):
            #    self.save_state()

            # Calculate seconds since last tick
            now = time.time()
            duration_seconds = 0
            if self.last_tick_time != 0:
                duration_seconds = now - self.last_tick_time
            self.last_tick_time = now

            # Tick all subsystems
            #print "DEBUG: tick #%d, %f seconds since last one" % (self.tick_count, duration_seconds)
            return self.reactor.tick(duration_seconds)

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def quit(self):
        return self.launcher_instance.quit()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def reload(self):
        return self.launcher_instance.reload()

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def run(self):
        print "RUNNING"
        self.is_running = True
        # Set the reactor to tick every N ms
        gobject.timeout_add(self.config['simulation']['tick_interval'], self.tick)

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def reset(self):
        """Resets the simulation to startinng conditions"""
        if self.reactor:
            self.reactor.unload()
            del(self.reactor)
        else:
            print "RESETTING"
        self.reactor = reactor.reactor(self, self.dbus_object_path)
        self.reactor.load_layout(reactor.default_layout, reactor.default_depth)
        self.tick_count = 0
        self.last_tick_time = 0
        
        # Finally emit the reset signal
        self.emit_simulation_reset(self.dbus_object_path)

    @dbus.service.signal('fi.hacklab.reactorsimulator.engine')
    def emit_simulation_reset(self, sender):
        pass

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def pause(self):
        """Just sets an internal variable to control ticks"""
        print "PAUSED"
        self.is_running = False

    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def save_state(self, name=''):
        if not name:
            name = 'latest'
        path = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ), "%s.state" % name)
        # TODO: Figure out some handy way to serialize the reactor state (and if case someone forgot pickle won't work)
        #with open(path, 'w') as f:
        
    @dbus.service.method('fi.hacklab.reactorsimulator.engine')
    def load_state(self, name=''):
        if not name:
            name = 'latest'
        path = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ), "%s.state" % name)
        #with open(path) as f:
            # TODO: Do we need to unload first ?

    def config_reloaded(self):
        self.reactor.config_reloaded()
        print "CONFIG RELOADED"
