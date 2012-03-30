import dbus.service

class baseclass(dbus.service.Object):
    def __init__(self, config, launcher_instance, **kwargs):
        self.config = config
        self.launcher_instance = launcher_instance
        self.mainloop = self.launcher_instance.mainloop
        self.bus = self.launcher_instance.bus
        if not kwargs.has_key('dbus_interface_name'):
            kwargs['dbus_interface_name'] = kwargs['dbus_default_interface_name']
        if not kwargs.has_key('dbus_object_path'):
            kwargs['dbus_object_path'] = "/%s" % kwargs['dbus_interface_name'].replace('.', '/')
        self.dbus_object_path = kwargs['dbus_object_path']
        self.dbus_interface_name = kwargs['dbus_interface_name']
        # Start the DBUS stuff
        dbus.service.Object.__init__(self, dbus.service.BusName(self.dbus_interface_name, bus=self.bus), self.dbus_object_path)
        
        #print "service baseclass initialized as %s:%s with config %s" % (self.dbus_interface_name, self.dbus_object_path, repr(self.config))


