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
        self.bus.add_signal_receiver(self.pca9535_changed, dbus_interface = "fi.hacklab.ardubus", signal_name = "pca9535_change")
        self.bus.add_signal_receiver(self.analog_changed, dbus_interface = "fi.hacklab.ardubus", signal_name = "aio_change")
        #self.bus.add_signal_receiver(self.switch_changed, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_change", path='/fi/hacklab/ardubus/arduino0')
        self.bus.add_signal_receiver(self.switch_report, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_report")
        self.bus.add_signal_receiver(self.analog_report, dbus_interface = "fi.hacklab.ardubus", signal_name = "aio_report")
        self.bus.add_signal_receiver(self.alias_changed, dbus_interface = "fi.hacklab.ardubus", signal_name = "alias_change")
        self.bus.add_signal_receiver(self.alias_report, dbus_interface = "fi.hacklab.ardubus", signal_name = "alias_report")

    def signal_received(self, *args, **kwargs):
        print "Got args: %s" % repr(args)
        print "Got kwargs: %s" % repr(kwargs)

    def switch_changed(self, pin, state, sender):
        print "Pin %d changed(index) to %d on %s" % (pin, state, sender)

    def pca9535_changed(self, pin, state, sender):
        print "PCA9535 Pin %d changed(index) to %d on %s" % (pin, state, sender)

    def alias_changed(self, alias, state, sender):
        print "Pin '%s' changed to %d on %s" % (alias, state, sender)

    def analog_changed(self, pin, value, sender):
        print "Analog pin(index) %d changed to %d on %s" % (pin, value, sender)

    def switch_report(self, pin, state, time, sender):
        #print "Pin(index) %d has been %d for %dms on %s" % (pin, state, time, sender)
        pass

    def analog_report(self, p_index, value, time, sender):
        print "Analog pin(index) %d has been %d for %dms on %s" % (p_index, value, time, sender)
        pass

    def alias_report(self, alias, value, time, sender):
        #print "Pin '%s' has been %d for %dms on %s" % (alias, value, time, sender)
        pass


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    listener = ardubus_listener(bus)


    loop = gobject.MainLoop()
    loop.run()
