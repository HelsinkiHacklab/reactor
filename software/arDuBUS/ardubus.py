#!/usr/bin/env python
# The real deal, this will talk with an arduino and pass signals/method calls back and forth
PIN_OFFSET=32 # We need to offset the pin numbers to CR and LF which are control characters to us (NOTE: this *must* be same in sketch)

import os,sys
import dbus
import dbus.service



class ardubus(dbus.service.Object):
    def __init__(self, bus, object_name, config):
        self.config = config
        self.object_name = object_name
        self.object_path = '/fi/hacklab/ardubus/' + object_name
        self.bus_name = dbus.service.BusName('fi.hacklab.ardubus', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)
        self.initialize_serial()

    def send_serial_command(self, command):
        command = command + "\n"
        for c in command:
            self.serial_port.write(c)
        self.serial_port.flush()
        # TODO Check for the ACK from board somehow (not exactly trivial when another thread is constantly reading the port for reports [though now the sketch acknowledges the command it parses in full so we could look into the history])
        print 'DEBUG: sent command %s' % repr(command)
        return True
        
    def p2b(self, pin):
        """Convert pin number integer to a byte to be sent to the sketch"""
        return chr(pin+PIN_OFFSET)

    @dbus.service.method('fi.hacklab.ardubus')
    def hello(self):
        return "Hello,World! My name is " + self.object_name

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yy') # "y" is the signature for a byte
    def set_pwm(self, pin, cycle):
        if cycle in [ 13, 10]: #Offset values that map to CR or LF by one
            cycle += 1
        self.send_serial_command("P%s%s" % (self.p2b(pin), chr(cycle)))

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yy') # "y" is the signature for a byte
    def set_servo(self, sindex, value):
        """Note that the first value is NOT a pin number but index of the servos array on the sketch (so first servo is 0 etc), however Arduino does not have dictionaries we can't sensibly do lookup via the pin number"""
        if value in [ 13, 10]: #Offset values that map to CR or LF by one
            value += 1
        self.send_serial_command("S%s%s" % (self.p2b(sindex), chr(value)))

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yb') # "y" is the signature for a byte
    def set_dio(self, pin, state):
        if state:
            self.send_serial_command("D%s1" % self.p2b(pin))
        else:
            self.send_serial_command("D%s0" % self.p2b(pin))

    @dbus.service.signal('fi.hacklab.ardubus')
    def dio_change(self, pin, state, sender):
        #print "SIGNALLING: Pin %d changed to %d on %s" % (pin, state, sender)
        pass

    @dbus.service.signal('fi.hacklab.ardubus')
    def dio_report(self, pin, state, time, sender):
        #print "SIGNALLING: Pin %d has been %d for %dms on %s" % (pin, state, time, sender)
        pass


    def initialize_serial(self):
        import threading, serial
        print "initialize_serial called"
        self.input_buffer = ""
        serial_device = None
        #consoles have different configuration file structure
        if self.config.has_section('board'):
            serial_device = self.config.get('board', 'device')
        else:
            serial_device = self.config.get(self.object_name, 'device')
        self.serial_port = serial.Serial(serial_device, 115200, xonxoff=False, timeout=0.00001)
        self.receiver_thread = threading.Thread(target=self.serial_reader)
        self.receiver_thread.setDaemon(1)
        self.receiver_thread.start()
        print "thread started"

    def message_received(self, input_buffer):
        #print "message_received called with buffer %s" % repr(input_buffer)
        try:
            if (self.input_buffer[:2] == 'CD'):
                # State change
                self.dio_change(ord(input_buffer[2]), bool(int(input_buffer[3])), self.object_name)
                return
            if (self.input_buffer[:2] == 'RD'):
                # State report (FIXME: the integer parsing doesn't quite seem to work [probably need to fix the sketch as well])
                self.dio_report(ord(input_buffer[2]), bool(int(input_buffer[3])), int(input_buffer[5:], 16), self.object_name)
                pass
        except IndexError,e:
            print "message_received: Got exception %s" % e
            # Ignore indexerrors, they just mean we could not parse the command
            pass


    def serial_reader(self):
        import string,binascii
        alive = True
        try:
            while alive:
                if not self.serial_port.inWaiting():
                    # Don't try to read if there is no data.
                    continue
                data = self.serial_port.read(1)
                if len(data) == 0:
                    continue
                # hex-encode unprintable characters
#               if data not in string.letters.join(string.digits).join(string.punctuation).join("\r\n"):
#                    sys.stdout.write("\\0x".join(binascii.hexlify(data)))
                # OTOH repr was better afterall
                if data not in "\r\n":
                    sys.stdout.write(repr(data))
                else:
                    sys.stdout.write(data)
                # Put the data into inpit buffer and check for CRLF
                self.input_buffer += data
                # Trim prefix NULLs and linebreaks
                self.input_buffer = self.input_buffer.lstrip(chr(0x0) + "\r\n")
                #print "input_buffer=%s" % repr(self.input_buffer)
                if (    len(self.input_buffer) > 1
                    and self.input_buffer[-2:] == "\r\n"):
                    # Got a message, parse it (sans the CRLF) and empty the buffer
                    self.message_received(self.input_buffer[:-2])
                    self.input_buffer = ""

        except serial.SerialException, e:
            print "Got exception %s" % e
            self.alive = False



if __name__ == '__main__':
    import dbus.mainloop.glib, gobject
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    import ConfigParser
    config = ConfigParser.SafeConfigParser()
    if not os.path.isfile('ardubus.conf'):
        config.add_section('arduino0')
        config.set('arduino0', 'device', '/dev/ttyUSB0')
        # TODO: Other defaults
        with open('ardubus.conf', 'wb') as configfile:
            config.write(configfile)
    config.read('ardubus.conf')

    bus = dbus.SessionBus()

    service_objects = {}
    for board_name in config.sections():
        service_objects[board_name] = ardubus(bus, board_name, config)

    loop = gobject.MainLoop()
    loop.run()
