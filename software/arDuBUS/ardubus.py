#!/usr/bin/env python

# The real deal, this will talk with an arduino and pass signals/method calls back and forth

import os,sys
import threading, serial
import gobject
gobject.threads_init()
import dbus
import dbus.service
import dbus.mainloop.glib
from dbus.mainloop.glib import threads_init
threads_init()



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
        pass

    def initialize_serial(self):
        print "initialize_serial called"
        self.input_buffer = []
        self.serial_port = serial.Serial(self.config.get(self.object_name, 'device'), 115200, xonxoff=False, timeout=0.00001)
        self.receiver_thread = threading.Thread(target=self.serial_reader)
        self.receiver_thread.setDaemon(1)
        self.receiver_thread.start()
        print "thread started"

    def message_received(self):
        pass

    def serial_reader(self):
        import string,binascii
        print "Serial reader thread"
        alive = True
        try:
            while alive:
                data = self.serial_port.read(1)
                if len(data) == 0:
                    continue
                # hex-encode unprintable characters
                if data not in string.letters.join(string.digits).join(string.punctuation).join("\r\n"):
                    sys.stdout.write("\\0x".join(binascii.hexlify(data)))
                else:
                    sys.stdout.write(data)
                # Put the data into inpit buffer and check for CRLF
                self.input_buffer.append(data)
                if (    len(self.input_buffer) > 1
                    and self.input_buffer[-2:] == "\r\n"):
                    # Got a message, parse it and empty the buffer
                    self.message_received()
                    self.input_buffer = []

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
