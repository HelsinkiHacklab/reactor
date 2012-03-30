from __future__ import with_statement
import sys,os,signal
import yaml
import dbus,dbus.service,gobject

class baseclass(dbus.service.Object):
    def __init__(self, mainloop, bus, **kwargs):
        # These we will need (and will pass on)
        self.mainloop = mainloop
        self.bus = bus
        
        # Some sanity-checking and automation
        if not kwargs.has_key('dbus_launcher_interface_name'):
            kwargs['dbus_launcher_interface_name'] = kwargs['dbus_default_interface_name'] + '.launcher'
        if not kwargs.has_key('dbus_launcher_object_path'):
            kwargs['dbus_launcher_object_path'] = "/%s" % kwargs['dbus_launcher_interface_name'].replace('.', '/')
        self.dbus_object_path = kwargs['dbus_launcher_object_path']
        self.dbus_interface_name = kwargs['dbus_launcher_interface_name']
        # Start the DBUS stuff
        dbus.service.Object.__init__(self, dbus.service.BusName(self.dbus_interface_name, bus=self.bus), self.dbus_object_path)
        
        # Load config
        if kwargs.has_key('config_file_path'):
            self.config_file_path = kwargs['config_file_path']
        else:
            self.config_file_path = None
        self.load_config()

        # If the class was defined import that too
        if kwargs.has_key('main_class_name'):
            exec("from %s import %s as main_class" % (kwargs['main_class_name'],kwargs['main_class_name']))
            self.main_instance = main_class(self.config, self, **kwargs)
        else:
            self.main_instance = None

    def hook_signals(self):
        """Hooks common UNIX signals to corresponding handlers"""
        signal.signal(signal.SIGTERM, self.quit)
        signal.signal(signal.SIGQUIT, self.quit)
        signal.signal(signal.SIGHUP, self.reload)

    def quit(self):
        """Quits the mainloop"""
        self.mainloop.quit()

    def reload(self):
        """Used to reload the config (and if we have """
        self.load_config()
        # Seems we need to explicitly refresh this
        if self.main_instance:
            self.main_instance.config = self.config

    def load_config(self):
        """Loads (or reloads) the configuration file"""
        if not self.config_file_path:
            return False
        with open(self.config_file_path) as f:
            self.config = yaml.load(f)
        return True
