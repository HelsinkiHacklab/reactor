import os,sys,math
import dbus
import dbus.service
import threading,signal
from visualizer import reactor_visualizer


if __name__ == '__main__':
    import dbus.mainloop.glib, gobject
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    
    bus = dbus.SessionBus()
    loop = gobject.MainLoop()
    listener = reactor_visualizer.reactor_listener(bus, loop)


    signal.signal(signal.SIGTERM, listener.quit)
    signal.signal(signal.SIGQUIT, listener.quit)
    signal.signal(signal.SIGHUP, listener.reset_state)

    # Run visualizer in own thread
    listener.start()

    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()


