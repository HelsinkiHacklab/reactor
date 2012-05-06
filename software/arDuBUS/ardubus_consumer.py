#!/usr/bin/env python -i
import dbus,time
 
bus = dbus.SessionBus()
launcher = bus.get_object('fi.hacklab.ardubus.launcher', '/fi/hacklab/ardubus/launcher')
print launcher.list_boards()

p = bus.get_object('fi.hacklab.ardubus.launcher', '/fi/hacklab/ardubus/aliases_test_board')
