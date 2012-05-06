#!/usr/bin/env python
# The real deal, this will talk with an arduino and pass signals/method calls back and forth
from __future__ import with_statement
# Boilerplate to add ../pythonlibs (via full path resolution) to import paths
import os,sys
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)

# Import our DBUS service module
import service,dbus,binascii,time

# We need to offset the pin numbers to CR and LF which are control characters to us (NOTE: this *must* be same as in ardubus.h)
PIN_OFFSET=32 

class ardubus(service.baseclass):
    def __init__(self, config, launcher_instance, **kwargs):
        super(ardubus, self).__init__(config, launcher_instance, **kwargs)
        self.object_name = kwargs['device_name']
        self.serial_device = kwargs['serial_device']
        self.serial_speed = kwargs['serial_speed']
        self.config_reloaded() # Triggers all config normalizations and mapping rebuilds
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

    def normalize_pins(self, config_section):
        """Normalizes a pin config to dict with pin ans alias keys"""
        #print "normalize_pins: BEFORE %s" % config_section
        if type(config_section) == list:
            keys = range(len(config_section))
        if type(config_section) == dict:
            keys = config_section.keys
        for k in keys:
            item = config_section[k]
            if type(item) != dict:
                item = { 'pin': item }
            # Make sure this key exists
            if not item.has_key('alias'):
                item['alias'] = None
            config_section[k] = item
        #print "normalize_pins: AFTER %s" % config_section
        return config_section

    def normalize_config(self):
        if self.config.has_key('digital_in_pins'):
            self.config['digital_in_pins'] = self.normalize_pins(self.config['digital_in_pins'])
        if self.config.has_key('pca9535_inputs'):
            self.config['pca9535_inputs'] = self.normalize_pins(self.config['pca9535_inputs'])
        # reminder to support output aliasing in the future, somehow...
        #if self.config.has_key('pca9535_outputs'):
        #    self.config['pca9535_outputs'] = self.normalize_pins(self.config['pca9535_outputs'])
        
        pass

    def rebuild_alias_maps(self):
        # When we support aliasing of output pins we need to map the aliases to correct io methods somehow...
        pass

    def config_reloaded(self):
        """Recalculates all config mappings etc"""
        self.normalize_config()
        self.rebuild_alias_maps()

    def stop_serial(self):
        self.serial_alive = False
        self.receiver_thread.join()
        self.serial_port.close()

    @dbus.service.method('fi.hacklab.ardubus')
    def quit(self):
        """Closes the serial port and unloads from DBUS"""
        self.stop_serial()
        self.remove_from_connection()

    @dbus.service.method('fi.hacklab.ardubus')
    def hello(self):
        return "Hello,World! My name is " + self.object_name

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yy') # "y" is the signature for a byte
    def set_pwm(self, pwm_index, cycle):
        if cycle in [ 13, 10]: #Offset values that map to CR or LF by one
            cycle += 1
        self.send_serial_command("P%s%s" % (self.p2b(pwm_index), chr(cycle)))

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yyy') # "y" is the signature for a byte
    def set_jbol_pwm(self, jbol_index, ledno, cycle):
        if cycle in [ 13, 10]: #Offset values that map to CR or LF by one
            cycle += 1
        self.send_serial_command("J%s%s%s" % (self.p2b(jbol_index), self.p2b(ledno), chr(cycle)))

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yy') # "y" is the signature for a byte
    def set_servo(self, servo_index, value):
        if value > 180:
            value = 180 # Servo library accepts values from 0 to 180 (degrees)
        if value in [ 13, 10]: #Offset values that map to CR or LF by one
            value += 1
        self.send_serial_command("S%s%s" % (self.p2b(servo_index), chr(value)))

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yn') # "y" is the signature for a byte, n is 16bit signed integer
    def set_servo_us(self, servo_index, value):
        self.send_serial_command("s%s%s" % (self.p2b(servo_index), "%04X" % int(value)))


    @dbus.service.method('fi.hacklab.ardubus', in_signature='yb') # "y" is the signature for a byte
    def set_595bit(self, bit_index, state):
        if state:
            self.send_serial_command("B%s1" % self.p2b(bit_index))
        else:
            self.send_serial_command("B%s0" % self.p2b(bit_index))

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yy') # "y" is the signature for a byte
    def set_595byte(self, reg_index, state):
        self.send_serial_command("W%s%s" % (self.p2b(reg_index), binascii.hexlify(str(state)).upper()))

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yb') # "y" is the signature for a byte
    def set_dio(self, digital_index, state):
        if state:
            self.send_serial_command("D%s1" % self.p2b(digital_index))
        else:
            self.send_serial_command("D%s0" % self.p2b(digital_index))

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yb') # "y" is the signature for a byte
    def set_pca9535_bit(self, digital_index, state):
        if state:
            self.send_serial_command("E%s1" % self.p2b(digital_index))
        else:
            self.send_serial_command("E%s0" % self.p2b(digital_index))

    @dbus.service.method('fi.hacklab.ardubus', in_signature='yy') # "y" is the signature for a byte
    def set_pca9535_byte(self, reg_index, state):
        return False
        # TODO: implement
        # example from 595
        #self.send_serial_command("W%s%s" % (self.p2b(reg_index), binascii.hexlify(str(state)).upper()))

    @dbus.service.signal('fi.hacklab.ardubus')
    def alias_change(self, alias, state, sender):
        """Aliased pin has changed state"""
        #print "SIGNALLING: %s changed to %d on %s" % (alias, state, sender)
        pass

    @dbus.service.signal('fi.hacklab.ardubus')
    def dio_change(self, p_index, state, sender):
        if self.config['digital_in_pins'][p_index]['alias']:
            self.alias_change(self.config['digital_in_pins'][p_index]['alias'], state, sender)
        pass

    @dbus.service.signal('fi.hacklab.ardubus')
    def pca9535_change(self, p_index, state, sender):
        #print "SIGNALLING: Pin(index) %d changed to %d on %s" % (p_index, state, sender)
        if self.config['pca9535_inputs'][p_index]['alias']:
            self.alias_change(self.config['pca9535_inputs'][p_index]['alias'], state, sender)
        pass

    @dbus.service.signal('fi.hacklab.ardubus')
    def dio_report(self, p_index, state, time, sender):
        #print "SIGNALLING: Pin(index) %d has been %d for %dms on %s" % (p_index, state, time, sender)
        pass

    @dbus.service.signal('fi.hacklab.ardubus')
    def pca9535_report(self, p_index, state, time, sender):
        #print "SIGNALLING: Pin(index) %d has been %d for %dms on %s" % (p_index, state, time, sender)
        pass

    @dbus.service.signal('fi.hacklab.ardubus')
    def aio_change(self, p_index, value, sender):
        #print "SIGNALLING: Analog-pin(index) %d changed to %d on %s" % (p_index, value, sender)
        pass

    @dbus.service.signal('fi.hacklab.ardubus')
    def aio_report(self, p_index, value, time, sender):
        #print "SIGNALLING: Analog-pin(index) %d has been %d for %dms on %s" % (p_index, value, time, sender)
        pass


    def initialize_serial(self):
        import threading, serial
        print "initialize_serial called"
        self.input_buffer = ""
        self.serial_port = serial.Serial(self.serial_device, self.serial_speed, xonxoff=False, timeout=0.00001)
        self.receiver_thread = threading.Thread(target=self.serial_reader)
        self.receiver_thread.setDaemon(1)
        self.receiver_thread.start()
        print "%s serial thread started" % self.dbus_object_path

    def message_received(self, input_buffer):
        #print "message_received called with buffer %s" % repr(input_buffer)
        try:
            if (self.input_buffer[:2] == 'CD'):
                # State change
                self.dio_change(ord(input_buffer[2]), bool(int(input_buffer[3])), self.object_name)
                return
            if (self.input_buffer[:2] == 'CP'):
                # State change
                self.pca9535_change(ord(input_buffer[2]), bool(int(input_buffer[3])), self.object_name)
                return
            if (self.input_buffer[:2] == 'RD'):
                self.dio_report(ord(input_buffer[2]), bool(int(input_buffer[3])), int(input_buffer[4:12], 16), self.object_name)
                pass
            if (self.input_buffer[:2] == 'RP'):
                self.pca9535_report(ord(input_buffer[2]), bool(int(input_buffer[3])), int(input_buffer[4:12], 16), self.object_name)
                pass
            if (self.input_buffer[:2] == 'CA'):
                self.aio_change(ord(input_buffer[2]), int(input_buffer[3:7], 16), self.object_name)
                pass
            if (self.input_buffer[:2] == 'RA'):
                self.aio_report(ord(input_buffer[2]), int(input_buffer[3:7], 16), int(input_buffer[6:15], 16), self.object_name)
                pass
        except Exception,e:
            print "message_received: Got exception %s" % e
            # Ignore indexerrors, they just mean we could not parse the command
            pass


    def serial_reader(self):
        import string,binascii
        import serial # We need the exceptions from here
        self.serial_alive = True
        try:
            while self.serial_alive:
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

        except (IOError, serial.SerialException), e:
            print "Got exception %s" % e
            self.serial_alive = False
            # It seems we cannot really call this from here, how to detect the problem in main thread ??
            #self.launcher_instance.unload_device(self.object_name)

if __name__ == '__main__':
    print "Use ardbus_launcher.py"
    sys.exit(1)
