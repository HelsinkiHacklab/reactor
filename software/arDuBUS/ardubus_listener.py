# A trivial example for listening signals on the bus

import gobject
import dbus
import dbus.service
import dbus.mainloop.glib


class ardubus_listener():
    def __init__(self, bus):
        self.bus = bus
        # We can either listen all signals on the interface regardles of the board or specify we want to listen only to specific board
        self.bus.add_signal_receiver(self.switch_changed, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_change")
        #self.bus.add_signal_receiver(self.switch_changed, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_change", path='/fi/hacklab/ardubus/arduino0')
        self.bus.add_signal_receiver(self.switch_report, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_report")

    def signal_received(self, *args, **kwargs):
        print "Got args: %s" % repr(args)
        print "Got kwargs: %s" % repr(kwargs)

    def switch_changed(self, pin, state, sender):
        print "Pin %d changed to %d on %s" % (pin, state, sender)

    def switch_report(self, pin, state, time, sender):
        print "Pin %d has been %d for %dms on %s" % (pin, state, time, sender)


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    listener = ardubus_listener(bus)


    loop = gobject.MainLoop()
    loop.run()
