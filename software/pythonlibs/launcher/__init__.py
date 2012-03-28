import sys,os
from baseclass import *


def main(launcherclass, **kwargs):
    """Boilerplate main program check, .launcher will be added to the interface by the baseclass and path generated from the interface"""
    # Enable threading using glib mainloop
    import dbus,gobject,dbus.mainloop.glib
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    
    # Get the bus and mainloop
    bus = dbus.SessionBus()
    loop = gobject.MainLoop()

    # If no launcher specified use the baseclass one    
    if not launcherclass:
        launcherclass = baseclass
    instance = launcherclass(loop, bus, **kwargs)
    # And start the eventloop (catch KeyboardInterrupt here for [hopefully] clean mainloop quit)
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()
