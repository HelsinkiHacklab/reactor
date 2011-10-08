import sys 
import threading
import serial
import gobject 

import dbus
import dbus.service
import dbus.mainloop.glib

import ConfigParser

import ardubus

#NOTE: this will be just signal wrapper generator layer between lower ardubus and 
#game components
#this could be seperate entinty and just relay upper level signals to lower level signals
#instead of being derivate and calling methods directly, but that might be little overkill 

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
                if len(input_act) >=3:
                    receiver = self.make_interpolate(int(input_act[2]), 
                                                     int(input_act[3]), 
                                                     receiver)
            else:
                receiver = self.__getattribute__(input_act[0])
            
            self.bus.add_signal_receiver(receiver, dbus_interface = "fi.hacklab.ardubus", 
                                         signal_name = input[0])

        for output in config.items('outputs'):
            print "setting signal", output[0], "for command", output[1]
            #TODO: mapping user inputs from arduino into signals
            #self.__dict__[output[0]] = dbus.service.signal('fi.hacklab.ardubus')(self.tmp)            
            #print "%s" % repr(self.__dict__[output[0]])
            #self.__dict__[output[0]]()
    
    def call_with_offset(self, offset, method):
        def _m(num, *args):
            method(num + offset, *args)
        return _m

    def make_interpolate(self, vmin, vmax, method):
        scale = float(180) / float(vmax - vmin)
        def _m(index, value, *args):
            method(index, int( (value - vmin)*scale), *args)
        return _m
  
    #override default signal generators with handlers  
    def dio_change(self, pin, state, sender):
        #self.dios[pin](state) #call singal method for this pin change 
        #print "SIGNALLING: Pin %d changed to %d on %s" % (pin, state, sender)
        pass

    def dio_report(self, pin, state, time, sender):
        #print "SIGNALLING: Pin %d has been %d for %dms on %s" % (pin, state, time, sender)
        pass
  
    def aio_change(self, pin, value, sender):
        #print "SIGNALLING: Pin %d has been %d for %dms on %s" % (pin, state, time, sender)
         pass

    #examples of mappers called from signals 
    def dbg_receive_signal(self, *args, **kwargs):
        print "Got args: %s" % repr(args)
        print "Got kwargs %s" % repr(kwargs)
    
    #these will be deprecated, methods that communicate with arduino sketch
    #from base class will be used
    def gauge_display(self, gnumber, value):
        print "deprecated"
        #command servo gauge to display value here 
        #self.send_serial_command("SG%d:%d" % (gnumber, value))

    def set_led(self, lnumber, state):
        print "deprecated"
        #command led to state on,off,flicker here 
        #self.send_serial_command("SL%d:%d" % (lnumber, state))

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

