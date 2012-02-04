#!/usr/bin/env python -i
import dbus,time
 
bus = dbus.SessionBus()
nm = bus.get_object('fi.hacklab.noisemaker', '/fi/hacklab/noisemaker/noisemaker0')

nm.play_sample('kathunk.wav')

#nm.start_sequence('test1','test1_loopid0')
#nm.stop_sequence('test1_loopid0')
