#!/usr/bin/env python -i
import dbus,time
 
bus = dbus.SessionBus()
nm = bus.get_object('fi.hacklab.noisemaker', '/fi/hacklab/noisemaker/noisemaker0')

#nm.play_sample('kathunk.wav')

#nm.start_sequence('features_test','features_test0')
#nm.stop_sequence('features_test0')
nm.start_sequence('loop_only','loop_only0')
print nm.list_loops()
#nm.stop_sequence('loop_only0')
#nm.start_sequence('startend_only','startend_only0')
#nm.stop_sequence('startend_only0')
