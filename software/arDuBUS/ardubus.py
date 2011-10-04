#!/usr/bin/env python

# The real deal, this will talk with an arduino and pass signals/method calls back and forth

import os
import gobject
import dbus
import dbus.service
import dbus.mainloop.glib
import threading, serial

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
        # TODO: initialize serial connection listener to a separate thread
        self.input_buffer = []
        self.serial_port = serial.Serial(self.config.get(self.board_name, 'device'), 115200, xonxoff=False, timeout=0.00001)
        self.receiver_thread = threading.Thread(target=self.serial_reader)
        self.receiver_thread.setDaemon(1)
        self.receiver_thread.start()

    def message_received(self):
        pass

    def serial_reader(self):
        alive = True
        try:
            while alive:
                data = self.serial_port.read(1)
                # TODO: hex-encode unprintable characters
                if data not in ["\r", "\n"]:
                    sys.stdout.write(repr(data))
                else:
                    sys.stdout.write(data)
                input_buffer.append(data)
                if (    len(self.input_buffer) > 1
                    and self.input_buffer[-2:] == "\r\n"):
                    # Got a message, parse it and empty the buffer
                    self.message_received()
                    self.input_buffer = []

        except serial.SerialException, e:
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
