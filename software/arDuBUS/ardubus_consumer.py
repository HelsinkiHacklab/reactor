#!/usr/bin/env python -i
import dbus,time
 
bus = dbus.SessionBus()
arduino0 = bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino0')
hello0 = arduino0.get_dbus_method('hello', 'fi.hacklab.ardubus')
pwm0 = arduino0.get_dbus_method('set_pwm', 'fi.hacklab.ardubus')
dio0 = arduino0.get_dbus_method('set_dio', 'fi.hacklab.ardubus')
servo0 = arduino0.get_dbus_method('set_servo', 'fi.hacklab.ardubus')
servo_us0 = arduino0.get_dbus_method('set_servo_us', 'fi.hacklab.ardubus')
jbol0 = arduino0.get_dbus_method('set_jbol_pwm', 'fi.hacklab.ardubus')
ch595bit = arduino0.get_dbus_method('set_595bit', 'fi.hacklab.ardubus')
ch595byte = arduino0.get_dbus_method('set_595byte', 'fi.hacklab.ardubus')
print hello0()
pwm0(0,128)

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
namemap = dict(
  (v,k) for k,v in servomap.items()
)

def named_servo(name, ms):
    servo = namemap[name]
    servo_us0(servo, ms)

def all(deg):
    for servo in servos:
        servo0(servo,deg)

def all_us(pos):
    for servo in servos:
        servo_us0(servo,pos)

