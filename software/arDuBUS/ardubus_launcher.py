#!/usr/bin/env python
# Boilerplate to add ../pythonlibs (via full path resolution) to import paths
import os,sys
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)
# Import the launcher and other needed modules
import launcher,dbus,serial,time,re,yaml
# Import the ardbubus main class to be used directly
from ardubus import ardubus

# Define some values that will be used
my_signature = 'fi.hacklab.ardubus'
launcher_config = {
    'dbus_default_interface_name': my_signature,
    'config_file_path': os.path.realpath(__file__).replace('_launcher.py', '.yml'),
}

# Basic pass-through implementation
class my_launcher(launcher.baseclass):
    def __init__(self, mainloop, bus, **kwargs):
        super(my_launcher, self).__init__(mainloop, bus, **kwargs)

        self.board_ident_timeout = 4
        self.board_ident_regex = re.compile(r"\r\nBoard: (\w+) initializing\r\n")
        self.device_objects = {}
        self.scan()

        print "launcher initialized as %s:%s with config %s" % (self.dbus_interface_name, self.dbus_object_path, repr(self.config))

    # Override this method to load device configs too
    def load_config(self):
        super(my_launcher, self).load_config()
        self.device_config_file = os.path.join(os.path.dirname(self.config_file_path), 'devices.yml')
        self.devices_config = {}
        with open(self.device_config_file) as f:
            self.devices_config = yaml.load(f)
        return True

    @dbus.service.method(my_signature + '.launcher')
    def unload_device(self, device_name):
        self.device_objects[device_name].quit()
        del(self.device_objects[device_name])
        
    @dbus.service.method(my_signature + '.launcher')
    def list_boards(self):
        """Lists the currently known boards"""
        ret = self.device_objects.keys()
        if len(ret) == 0:
            return None
        return ret

    @dbus.service.method(my_signature + '.launcher')
    def quit(self):
        for device_name in self.device_objects.keys():
            self.unload_device(device_name)
        launcher.baseclass.quit(self)

    @dbus.service.method(my_signature + '.launcher')
    def reload(self):
        """Reloads device configs but *does not* rescan serial devices"""
        launcher.baseclass.reload(self)
        for device_name in self.device_objects.keys():
            if  not self.devices_config.has_key(device_name):
                print "We no longer have config for active device %s, skipping it" % device_name
                continue
            self.device_objects[device_name].config = self.devices_config[device_name]
            self.device_objects[device_name].config_reloaded()

    @dbus.service.method(my_signature + '.launcher')
    def start_board(self, serial_device, device_name):
        """Spins up an interface object for given board"""
        if not self.devices_config.has_key(device_name):
            print "Found device %s in port %s but there is no config in devices.yml" % (device_name, serial_device)
            return False
        if self.device_objects.has_key(device_name):
            print "Found device %s in port %s but it's already initialized as service" % (device_name, serial_device)
            return False
        self.device_objects[device_name] = ardubus(self.devices_config[device_name], self, device_name=device_name, dbus_object_path=self.dbus_object_path.replace('/launcher', "/%s" % device_name), serial_device=serial_device, serial_speed=self.config['speed'], dbus_interface_name="fi.hacklab.ardubus.%s" % device_name)
        return True

    def test_port(self, serial_device):
        """Tests a given device for a board and if found will spin off a service object for it"""
        try:
            port = serial.Serial(serial_device, self.config['speed'], xonxoff=False, timeout=0.01)
            # PONDER: are these the right way around...
            port.setDTR(False) # Reset the arduino by driving DTR for a moment (RS323 signals are active-low)
            time.sleep(0.050)
            port.setDTR(True)
            in_buffer = ""
            started = time.time()
            while True:
                data = port.read(1)
                in_buffer += data
                match = self.board_ident_regex.search(in_buffer)
                if not match:
                    # Timeout, abort
                    if ((time.time() - started) > self.board_ident_timeout):
                        print "Could not find board in %s in %d seconds" % (serial_device, self.board_ident_timeout)
                        print "buffer: %s" % repr(in_buffer)
                        port.close()
                        return False
                    # Otherwise go back to reading data
                    continue
                # Got a match, continue by setting up a new service object
                port.close() # Free the port
                device_name = match.group(1)
                if (self.start_board(serial_device, device_name)):
                    print "Found board %s in %f seconds" % (device_name, time.time() - started)
                    return True
                #otherwise init failed
                return False
        except serial.SerialException, e:
            # Problem with port
            print "Got an exception from port %s: %s" % (serial_device, repr(e))
            return False
        # Something weird happened, we should not drop this far
        print False

    @dbus.service.method(my_signature + '.launcher')
    def scan(self):
        """Scans the configured serial devices for boards"""
        for comport in self.config['search_ports']:
            self.test_port(comport)

    @dbus.service.method(my_signature + '.launcher')
    def rescan(self):
        """Quits all active devices and then scans serial devices again"""
        for device_name in self.device_objects.keys():
            self.unload_device(device_name)
        self.scan()

# Another small bit of boilerplate
if __name__ == '__main__':
    launcher.main(my_launcher, **launcher_config)
