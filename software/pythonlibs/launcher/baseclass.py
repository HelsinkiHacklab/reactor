from __future__ import with_statement
import sys,os,signal
import yaml
import dbus,dbus.service,gobject

class baseclass(dbus.service.Object):
    def __init__(self, mainloop, bus, **kwargs):
        self.mainloop = mainloop
        self.bus = bus
        
        if not kwargs.has_key('dbus_interface_name'):
            kwargs['dbus_interface_name'] = kwargs['dbus_default_interface_name'] + '.launcher'
        if not kwargs.has_key('dbus_object_path'):
            kwargs['dbus_object_path'] = "/%s" % kwargs['dbus_interface_name'].replace('.', '/')
        self.dbus_object_path = kwargs['dbus_object_path']
        self.dbus_interface_name = kwargs['dbus_interface_name']
        dbus.service.Object.__init__(self, dbus.service.BusName(self.dbus_interface_name, bus=self.bus), self.dbus_object_path)

    def quit(self):
        """Quits the mainloop"""
        self.mainloop.quit()

    def load_config(self):
        """Loads (or reloads) the configuration file"""
        
        pass
