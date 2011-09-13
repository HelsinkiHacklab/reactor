import gobject
import dbus
import dbus.service
import dbus.mainloop.glib


class ardubus_listener():
    def __init__(self, bus):
        self.bus = bus
        self.bus.add_signal_receiver(self.signal_received, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_change")

    def signal_received(self, *args, **kwargs):
        print "Got args: %s" % repr(args)
        print "Got kwargs: %s" % repr(kwargs)

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    listener = ardubus_listener(bus)


    loop = gobject.MainLoop()
    loop.run()
