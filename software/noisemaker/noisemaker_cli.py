#!/usr/bin/env python -i
import dbus,time
 
bus = dbus.SessionBus()
nm = bus.get_object('fi.hacklab.noisemaker', '/fi/hacklab/noisemaker/noisemaker0')

nm.play_sample('kathunk.wav')

