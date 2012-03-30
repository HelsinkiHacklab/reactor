import os,sys,math
import dbus
import dbus.service
import threading
from visualizer import reactor_visualizer


if __name__ == '__main__':
    import dbus.mainloop.glib, gobject
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    
    bus = dbus.SessionBus()
    loop = gobject.MainLoop()
    listener = reactor_visualizer.reactor_listener(bus, loop)

    # Run visualizer in own thread
    listener.start()

    # TODO: Add some nicer way to exit than ctrl-c

    loop.run()


