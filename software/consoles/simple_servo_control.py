# A trivial example for listening signals on the bus

import gobject
import dbus
import dbus.service
import dbus.mainloop.glib


servos = range(0,30)+[34,36,38]
servomap = {
  0: '20-22', # 1500, 2400),
  1: '13-22', 
  2: '12-22',
  3: '21-21',
  4: '13-21',
  5: '11-21',
  6: '12-21',
  7: '21-20',
  8: '13-20',
  9: '22-20',
  10: '20-20',
  11: '13-12',
  12: '12-20',
  13: '11-12',
  14: '10-20',
  15: '22-12',
  16: '21-13',
  17: '20-12',
  18: '13-13',
  19: '12-12',
  20: '11-13',
  21: '10-12',
  22: '22-13',
  23: '21-11',
  24: '12-13',
  25: '13-11',
  26: '20-13',
  27: '11-11',
  28: '10-13',
  29: '20-11',
  34: '20-10',
  36: '13-10',
  38: '12-10',
}
named_servo_values = dict(
  (v, 900) for k,v in servomap.items()
)
servo_namemap = dict(
  (v,k) for k,v in servomap.items()
)

switch_states = {}

switch_servo_map = {
    42: ('13-13', 'down'),
    60: ('13-13', 'up'),
   
}

class ardubus_listener():
    def __init__(self, bus):
        self.bus = bus
        # We can either listen all signals on the interface regardles of the board or specify we want to listen only to specific board
        self.bus.add_signal_receiver(self.switch_changed, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_change")
        self.bus.add_signal_receiver(self.analog_changed, dbus_interface = "fi.hacklab.ardubus", signal_name = "aio_change")
        #self.bus.add_signal_receiver(self.switch_changed, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_change", path='/fi/hacklab/ardubus/arduino0')
        self.bus.add_signal_receiver(self.switch_report, dbus_interface = "fi.hacklab.ardubus", signal_name = "dio_report")
        self.bus.add_signal_receiver(self.analog_report, dbus_interface = "fi.hacklab.ardubus", signal_name = "aio_report")
	self.arduino0 = bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino0')
	self.servo_us0 = self.arduino0.get_dbus_method('set_servo_us', 'fi.hacklab.ardubus')
	gobject.timeout_add(100, self.update_servo_positions)


    def update_servo_positions(self):
	# todo: check switch states and adjust the corresponding gauge value, then set it via dbus
	for switch,state in switch_states.items():
	    if state: # Switches are pulled up, low level means switched on
		continue
	    # TODO: map switch k to servo
	    if switch_servo_map.has_key(switch):
		servo_name = switch_servo_map[switch][0]
		if switch_servo_map[switch][1] == 'down':
		   named_servo_values[servo_name] -= 10;
                else:
		   named_servo_values[servo_name] += 10;
                if named_servo_values[servo_name] < 600:
                   named_servo_values[servo_name] = 600
                if named_servo_values[servo_name] > 2400:
                   named_servo_values[servo_name] = 2400
                self.named_servo(servo_name, named_servo_values[servo_name])
	return True


    def named_servo(self, name, ms):
	servo = servo_namemap[name]
	self.servo_us0(servo, ms)

    def signal_received(self, *args, **kwargs):
        print "Got args: %s" % repr(args)
        print "Got kwargs: %s" % repr(kwargs)

    def switch_changed(self, pin, state, sender):
	switch_states[pin] = state
        print "Pin %d changed(index) to %d on %s" % (pin, state, sender)

    def analog_changed(self, pin, value, sender):
        print "Analog pin(index) %d changed to %d on %s" % (pin, value, sender)

    def switch_report(self, pin, state, time, sender):
        #print "Pin(index) %d has been %d for %dms on %s" % (pin, state, time, sender)
	pass
    def analog_report(self, p_index, value, time, sender):
        print "Analog pin(index) %d has been %d for %dms on %s" % (p_index, value, time, sender)
        pass


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    listener = ardubus_listener(bus)


    loop = gobject.MainLoop()
    loop.run()
