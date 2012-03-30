#!/usr/bin/env python -i
import dbus,time
 
bus = dbus.SessionBus()
sim = bus.get_object('fi.hacklab.reactorsimulator.engine', '/fi/hacklab/reactorsimulator/engine')
reactor = bus.get_object('fi.hacklab.reactorsimulator.engine', '/fi/hacklab/reactorsimulator/engine/reactor')

sim.pause()
#sim.reset()

print "call sim.quit() when done"
