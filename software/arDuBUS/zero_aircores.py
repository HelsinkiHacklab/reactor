#!/usr/bin/env python -i
import dbus,time
 
bus = dbus.SessionBus()
launcher = bus.get_object('fi.hacklab.ardubus.launcher', '/fi/hacklab/ardubus/launcher')
print launcher.list_boards()

def get_board(bname):
    return bus.get_object("fi.hacklab.ardubus.%s" % bname, "/fi/hacklab/ardubus/%s" % bname)

b = get_board('rod_control_panel')

def zero_all(pos=0):
   for cb in range(5):
       for cm in range(8):
           b.set_aircore_position(cb, cm, pos)

def reset(pos=0):
    launcher.reload()
    zero_all(pos)

reset()


