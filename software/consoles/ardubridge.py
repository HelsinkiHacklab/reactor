#
# THIS NEEDS SERIOUS REFACTORING FROM THE SCRATH!!!!
# this probably makes no any sense , no more...
#
import sys 
import threading
import serial
import gobject 

import dbus
import dbus.service
import dbus.mainloop.glib

import ConfigParser

import ardubus
from collections import namedtuple
import re
OutputSignal = namedtuple('OutputSignal', 'signal index pin')

#NOTE: this will be just signal wrapper generator layer between lower ardubus and 
#game components
#this could be seperate entinty and just relay upper level signals to lower level signals
#instead of being derivate and calling methods directly, but that might be little overkill 

class ardubus_console(ardubus.ardubus):
    def __init__(self, bus, config):
	ardubus.ardubus.__init__(self, bus, config.get('board', 'name'), config)

        self.bus = bus        
        self.switches = {}
        self.switch_states = {}
	self.receivers = {}
   
        for input in config.items('inputs'):
            print "setting", input[1], "for signal", input[0]
            input_act = input[1].split(', ')
            #either replace ConfigParser readable file to get rid of this
            #hackishmishm. or preferably define all indexes to be in continous range in arduino scetches!!
            #so we can set signal handler once here..
            insignal = re.search("([a-z,A-Z,_]*)", input[0]).group(1)
            receiver = None
            assert(len(input_act) == 7)
            #now we only care about one type 
            pinpin = int(input_act[1])
            receiver = self.map_called_method(int(input_act[2]),
                                              int(input_act[3]),
                                              int(input_act[4]),
                                              int(input_act[5]),
                                              int(input_act[6]),  
                                              self.__getattribute__(input_act[0]))                
            if insignal in self.receivers:
                if pinpin in self.receivers[insignal]: 
                   self.receivers[insignal][pinpin].append(receiver)
                else:
                   self.receivers[insignal][pinpin] = [receiver]
	    else:
		self.receivers[insignal]={pinpin:[receiver]}
            	self.bus.add_signal_receiver(self.make_it(insignal, self.handle_receiver), dbus_interface = "fi.hacklab.ardubus", 
                                         signal_name = insignal)

        for output in config.items('outputs'):
            print "setting signal", output[0], "for command", output[1]
            #convert dummy method to signal, signal name is from methods name
            foo = dbus.service.signal('fi.hacklab.ardubus')
            def _m(self, index, value):
               pass
            #print re.search("([a-z,A-Z,_]*)", output[0]).group(1) 
            _m.__name__ = re.search("([a-z,A-Z,_]*)",output[0]).group(1)
            btf = foo(_m)
            output_act = output[1].split(', ')
            #TODO: add other types of inputs
            if output_act[0] =='R':
                first_pin = int(output_act[1])
                last_pin = int(output_act[2])
                for i in range(first_pin, last_pin):
                   self.switches[i] = OutputSignal(btf, first_pin, 0)
            elif output_act[0] == 'S':
                first_pin = int(output_act[1])
                self.switches[first_pin] = OutputSignal(btf, first_pin, 0)
            elif output_act[0] == 'W':
                ard_pin = int(output_act[1])
                swt_pin = int(output_act[2])
                self.switches[ard_pin] = OutputSignal(btf, ard_pin, swt_pin)
                print "adding", ard_pin, swt_pin
	    else:
                raise Exception("unknown input mode", output_act[0])  

    def map_called_method(self, offset, vmin, vmax, omin, omax, method):
         scale = float(omax - omin) / float(vmax - vmin)
         def _m(index, value, *args):
             #print index, offset, value, omin, omax, vmin, vmax, method
             method(offset, int( omin + (value - vmin)*scale), *args)
         return _m

    def make_it(self, insignal, method):
        def _m(pin, *args):
           
           method(insignal, pin, *args)
        return _m

    def handle_receiver(self, signal, pin, *args):
        for r in self.receivers[signal][int(pin)]:
            print signal, r
            r(pin, *args)

    #override default signal generators with handlers  
    def dio_change(self, pin, state, sender):
        assert(pin in self.switches)
        self.switch_states[pin] = state
        self.switches[pin].signal(self, pin - self.switches[pin].index+self.switches[pin].pin, not state) 
	#print "SIGNALLING: Pin %d changed to %d on %s" % (pin, state, sender)
        pass

    def dio_report(self, pin, state, time, sender):
        if pin not in self.switches:
            print("Received report for unknown pin %s" % pin)
            return
        if pin in self.switch_states and self.switch_states[pin] != state:
		self.switches[pin].signal(self, pin - self.switches[pin].index+self.switches[pin].pin, not state)
        elif pin not in self.switch_states:
		self.switches[pin].signal(self, pin - self.switches[pin].index+self.switches[pin].pin, not state)
	self.switch_states[pin] = state
        #print "SIGNALLING: Pin %d has been %d for %dms on %s" % (pin, state, time, sender)
        pass
  
    def aio_change(self, pin, value, sender):
        #print "SIGNALLING: Pin %d has been %d for %dms on %s" % (pin, state, time, sender)
         pass

    
    def dbg_receive_signal(self, *args, **kwargs):
        print "Got args: %s" % repr(args)
        print "Got kwargs %s" % repr(kwargs)
    

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

