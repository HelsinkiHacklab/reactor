# -*- coding: utf-8 -*-
from __future__ import with_statement
import yaml
import dbus
import dbus.service
import sys, os

#import pygtk, gtk

import pygst, gobject
pygst.require("0.10")
import gst


class noisemaker(dbus.service.Object):
    def __init__(self, config, bus, object_name='noisemaker0'):
        self.config = config
        self.active_loops = {}

        # Resolve the full sample path
        self.samples_path = os.path.realpath(os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  self.config['general']['sample_dir']))
        if not os.path.isdir(self.samples_path):
            raise Exception("Configured sample path %s is invalid" % self.config['general']['sample_dir'])

        self.bus = bus
        
        self.object_name = object_name
        self.object_path = '/fi/hacklab/noisemaker/' + object_name
        self.bus_name = dbus.service.BusName('fi.hacklab.noisemaker', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)
        
        
        print "Initialized as dbus object %s, samples from %s" % (self.object_path, self.samples_path)

    @dbus.service.method('fi.hacklab.noisemaker')
    def hello(self):
        return "Hello,World! My name is " + self.object_name

    @dbus.service.method('fi.hacklab.noisemaker', in_signature='s')
    def play_sample(self, sample_name):
        sample_path = os.path.join(self.samples_path, sample_name)
        print "noisemaker: Playing %s via GST Alsa" % sample_path
        player = gst.parse_launch("filesrc location=\"%s\" ! decodebin !  audioconvert ! audioresample ! alsasink" % sample_path)
        player.set_state(gst.STATE_PLAYING)

    @dbus.service.method('fi.hacklab.noisemaker', in_signature='ss')
    def start_sequence(self, sequence_name, loop_id):
        """Will play the configured start sample of sequnce and then start looping the loop, caller must provide also the identifier that will be used for stopping the sequence"""
        sequence = self.config['sequences'][sequence_name]
        # TODO: Make separate sequence class that can handle the playlist correctly, now start and loop samples are played on top of each other
        if sequence['start']:
            self.play_sample(sequence['start'])
        sample_path = os.path.join(self.samples_path, sequence['loop'])
        self.active_loops[loop_id] = noisemaker_loop(sample_path, sequence, self)
        self.active_loops[loop_id].start()

    @dbus.service.method('fi.hacklab.noisemaker', in_signature='s')
    def stop_sequence(self, loop_id):
        """Will stop playing the loop identified with loop_id and then play the end sample of the corresponding sequence"""
        self.active_loops[loop_id].stop()
        del(self.active_loops[loop_id])

class noisemaker_loop:
    def __init__(self, sample_path, sequence_config, noisemaker_instance):
        self.loop_count = 0
        self.loop_to = -1
        self.sample_path = sample_path
        print "noisemaker_loop: Playing %s via GST Alsa" % sample_path
        self.player = gst.parse_launch("filesrc location=\"%s\" ! decodebin !  audioconvert ! audioresample ! alsasink" % self.sample_path)
        self.sequence = sequence_config
        self.nm = noisemaker_instance

        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)

    def on_eos(self, bus, msg):
        self.loop_count = self.loop_count+1
        if (   self.loop_to > 0
            and self.loop_count > self.loop_to):
            return self.stop()
        print "noisemaker_loop: Sample %s loop %d" % (self.sample_path, self.loop_count)
        self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, 0)
        
    def start(self):
        self.player.set_state(gst.STATE_PLAYING)
    
    def stop(self):
        self.player.set_state(gst.STATE_NULL)
        self.bus.remove_signal_watch()
        if self.sequence['end']:
            self.nm.play_sample(self.sequence['end'])



if __name__ == '__main__':
    # Read config
    with open(__file__.replace('.py', '.yml')) as f:
        config = yaml.load(f)

    # Initialize DBUS for us
    from dbus.mainloop.glib import DBusGMainLoop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    
    noisemaker_instance = noisemaker(config,bus)
    
    # TODO: Add some nicer way to exit than ctrl-c
    loop = gobject.MainLoop()
    loop.run()
    
    
