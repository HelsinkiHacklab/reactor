import sys 
import threading
import serial
import gobject 

import dbus
import dbus.service
import dbus.mainloop.glib

import ConfigParser

import ardubus

class ardubus_console(ardubus.ardubus):
    def __init__(self, bus, config):
	ardubus.ardubus.__init__(self, bus, config.get('board', 'name'), config)

        self.bus = bus        
        self.commands = {}
        for input in config.items('inputs'):
            print "setting", input[1], "for signal", input[0]
            input_act = input[1].split(', ')
            receiver = None
            if len(input_act) > 1:
                receiver = self.call_with_offset(int(input_act[1]), 
                                                 self.__getattribute__(input_act[0]))                
            else:
                receiver = self.__getattribute__(input_act[0])
            
            self.bus.add_signal_receiver(receiver, dbus_interface = "fi.hacklab.ardubus", 
                                         signal_name = input[0])

        for output in config.items('outputs'):
            print "setting signal", output[0], "for command", output[1]
            self.__dict__[input[0]] = dbus.service.signal('fi.hacklab.ardubus',
                                       self.__getattribute__(input[1]))
            
    def message_received(self, input_buffer):
        print "received message from serial: %s" %repr(input_buffer)

    #NOTE: we have to keep always id / item number as first parameter 
    def call_with_offset(self, offset, method):
        def _m(num, *args):
            method(num + offset, *args)
        return _m

    #examples of signals and handlers 
    

    #examples of mappers called from signals 
    def dbg_receive_signal(self, *args, **kwargs):
        print "Got args: %s" % repr(args)
        print "Got kwargs %s" % repr(kwargs)

    def gauge_display(self, gnumber, value):
        #command servo gauge to display value here 
        self.send_serial_command("SG%d:%d" % (gnumber, value))

    def set_led(self, lnumber, state):
        #command led to state on,off,flicker here 
        self.send_serial_command("SL%d:%d" % (lnumber, state))

# these might be optional
# simulator could always send all signal states 
# back to panels when resetting / resuming etc.    

    @dbus.service.method('fi.hacklab.ardubus')
    def reset(self):
        #TODO use this to reset console
        pass

    @dbus.service.method('fi.hacklab.ardubus')
    def resume(self):
        #TODO resume panel state
        pass 

    @dbus.service.method('fi.hacklab.ardubus')
    def save(self):
        #TODO use this to save panel state
        pass 


if __name__ == '__main__':
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    config = ConfigParser.SafeConfigParser()
    config.read(sys.argv[1])

    bus = dbus.SessionBus()
    console = ardubus_console(bus, config)

    loop = gobject.MainLoop()
    loop.run()

