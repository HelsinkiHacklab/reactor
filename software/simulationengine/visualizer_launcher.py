import os,sys,math
import dbus
import dbus.service
import visualizer


if __name__ == '__main__':
    import dbus.mainloop.glib, gobject
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    
    bus = dbus.SessionBus()
    loop = gobject.MainLoop()
    listener = visualizer.reactor_listener(bus, loop)


    # TODO: Add some nicer way to exit than ctrl-c
    listener.loop.run()

