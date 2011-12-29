#!/usr/bin/env python -i
import dbus,time,random,time
 
bus = dbus.SessionBus()
arduino2 = bus.get_object('fi.hacklab.ardubus', '/fi/hacklab/ardubus/arduino2')
jbol = arduino2.get_dbus_method('set_jbol_pwm', 'fi.hacklab.ardubus')
while(True):
    board = random.randint(0,1)
    led = random.randint(0,47)
    jbol(board,led,255)
    time.sleep(0.25)
    jbol(board,led,0)

