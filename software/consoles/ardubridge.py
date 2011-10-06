import sys 
import threading
import serial

import dbus
import dbus.service
import dbus.mainloop.glib

import ConfigParser
import gobject

class ardubus_console(dbus.service.Object):
    def __init__(self, bus, config):
        self.bus = bus
        
        self.object_name = config.get('board', 'name')
        self.object_path = '/fi/hacklab/ardubus/' + self.object_name
        self.bus_name = dbus.service.BusName('fi.hacklab.ardubus', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)
        
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
            
        self.input_buffer = ""
        self.serial_port = serial.Serial(config.get('board', 'device'), 
                                         115200, xonxoff=False, timeout=0.00001)
        self.receiver_thread = threading.Thread(target=self.serial_reader)
        self.receiver_thread.setDaemon(1)
        self.receiver_thread.start()

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
        self.serial_port.write("SG %d %d" % (gnumber, value))

    def set_led(self, lnumber, state):
        #command led to state on,off,flicker here 
        self.serial_port.write("SL %d %d" % (lnumber, state))

    def serial_reader(self):
        alive = True
        try:
            while alive:
                if not self.serial_port.inWaiting():
                    continue
                data = self.serial_port.read(1)
                if len(data) == 0:
                    continue
                self.input_buffer += data
                self.input_buffer = self.input_buffer.lstrip(chr(0x0) + "\r\n")
                if (len(self.input_buffer) > 1
                    and self.input_buffer[-2:] == "\r\n"):
                    self.commands[self.input_buffer[:2]](self.input_buffer[2:-2])
                    self.input_buffer = ""
                
        except serial.SerialException, e:
            print "Got exception %s" % e
            self.alive = False

    @dbus.service.method('fi.hacklab.ardubus')
    def reset(self):
        #TODO use this to reset console
        pass

# these might be optional
# simulator could always send all signals to set proper
# state when resuming / resetting etc.

    @dbus.service.method('fi.hacklab.ardubus')
    def resume(self):
        #TODO resume panel state
        pass 

    @dbus.service.method('fi.hacklab.ardubus')
    def save(self):
        #TODO use this to save panel state
        pass 


if __name__ == '__main__':
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    gobject.threads_init()

    config = ConfigParser.SafeConfigParser()
    config.read(sys.argv[1])

    bus = dbus.SessionBus()
    console = ardubus_console(bus, config)

    loop = gobject.MainLoop()
    loop.run()

