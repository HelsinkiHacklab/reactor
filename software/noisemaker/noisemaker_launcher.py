import yaml
import dbus
import dbus.service
import sys, os
import noisemaker
import gobject


if __name__ == '__main__':
    # Read config
    with open(__file__.replace('_launcher.py', '.yml')) as f:
        config = yaml.load(f)

    # Initialize DBUS for us
    from dbus.mainloop.glib import DBusGMainLoop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    
    noisemaker_instance = noisemaker.noisemaker(config,bus)
    
    # TODO: Add some nicer way to exit than ctrl-c
    loop = gobject.MainLoop()
    loop.run()
    
    
