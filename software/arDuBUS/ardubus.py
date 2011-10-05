#!/usr/bin/env python

# The real deal, this will talk with an arduino and pass signals/method calls back and forth

import os,sys
import threading, serial
import gobject
gobject.threads_init()
import dbus
import dbus.service
import dbus.mainloop.glib
dbus.mainloop.glib.threads_init()



class ardubus(dbus.service.Object):
    def __init__(self, bus, object_name, config):
        self.config = config
        self.object_name = object_name
        self.object_path = '/fi/hacklab/ardubus/' + object_name
        self.bus_name = dbus.service.BusName('fi.hacklab.ardubus', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)
        self.initialize_serial()

    @dbus.service.method('fi.hacklab.ardubus')
    def hello(self):
        return "Hello,World! My name is " + self.object_name

    @dbus.service.signal('fi.hacklab.ardubus')
    def dio_change(self, pin, state, sender):
        #print "SIGNALLING: Pin %d changed to %d on %s" % (pin, state, sender)
        pass

    @dbus.service.signal('fi.hacklab.ardubus')
    def dio_report(self, pin, state, time, sender):
        #print "SIGNALLING: Pin %d has been %d for %dms on %s" % (pin, state, time, sender)
        pass


    def initialize_serial(self):
        print "initialize_serial called"
        self.input_buffer = ""
        self.serial_port = serial.Serial(self.config.get(self.object_name, 'device'), 115200, xonxoff=False, timeout=0.00001)
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
