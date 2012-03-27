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
        self.active_loops[loop_id] = noisemaker_sequence(sequence, self, loop_id)
        self.active_loops[loop_id].start()

    @dbus.service.method('fi.hacklab.noisemaker', in_signature='s')
    def stop_sequence(self, loop_id):
        """Will stop playing the loop identified with loop_id and then play the end sample of the corresponding sequence"""
        self.active_loops[loop_id].stop_at_next()
        # Note that the sequence object will handle unloading since it can finish the loop by itself as well

    @dbus.service.method('fi.hacklab.noisemaker')
    def list_loops(self):
        """Returns a list of tuples (of loop ids and their states)"""
        ret = []
        for k, v in self.active_loops.iteritems():
            ret.append((k, v.state))
        if len(ret) == 0:
            return None
        return ret

class noisemaker_sequence:
    def __init__(self, sequence_config, noisemaker_instance, loop_id):
        self.loop_id = loop_id
        self.loop_count = 0
        self.loop_to = -1
        self.state = False

        self.sequence = self.normalize_config(sequence_config)
        self.nm = noisemaker_instance
        
        if self.sequence.has_key('loop_count'):
            self.loop_to = self.sequence['loop_count']

        if self.sequence['start']:
            self.init_player(self.sequence['start'])
            self.state = 'start'
        else:
            self.init_player(self.sequence['loop'])
            self.state = 'loop'

    def normalize_config(self, sequence_config):
        if not sequence_config.has_key('loop_count'):
            sequence_config['loop_count'] = -1
        if not sequence_config.has_key('start'):
            sequence_config['start'] = None
        if not sequence_config.has_key('end'):
            sequence_config['end'] = None
        if not sequence_config.has_key('loop'):
            sequence_config['loop'] = None
        return sequence_config

    def init_player(self, sample_name):
        self.sample_path = os.path.join(self.nm.samples_path, sample_name)
        self.player = gst.parse_launch("filesrc location=\"%s\" ! decodebin !  audioconvert ! audioresample ! alsasink" % self.sample_path)
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)

    def unload_player(self):
        self.player.set_state(gst.STATE_NULL)
        self.bus.remove_signal_watch()
        del(self.bus)
        del(self.player)

    def on_eos(self, bus, msg):
        # If already in loop, pass to that method
        if self.state == 'loop':
            return self.on_eos_loop(bus,msg)
        # Start sample finished, switch to loop
        if (    self.state == 'start'
            and self.sequence['loop']):
            self.unload_player()
            self.init_player(self.sequence['loop'])
            self.state = 'loop'
            self.player.set_state(gst.STATE_PLAYING)
        else:
            # not in loop and no loop sample specified, only on option remains
            return self.stop_via_end()

    def on_eos_loop(self, bus, msg):
        self.loop_count = self.loop_count+1
        if (   self.loop_to > 0
            and self.loop_count > self.loop_to):
            return self.stop_via_end()
        print "noisemaker_sequence: Sample %s loop %d" % (self.sample_path, self.loop_count)
        self.player.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, 0)

    def start(self):
        self.player.set_state(gst.STATE_PLAYING)

    def stop_at_next(self):
        """At the end of current loop play the stop sequence"""
        self.loop_to = self.loop_count

    def stop_via_end(self):
        """Immeadiate stop of loop and playing of end sample"""
        # TODO: use local pipeline and unload from active loops only when actually done
        self.unload_player()
        if self.sequence['end']:
            self.state = 'end'
            self.nm.play_sample(self.sequence['end'])
        # Unload from noisemakers active loops
        del(self.nm.active_loops[self.loop_id])


    def stop(self):
        """Immeadiate stop, no not play end sample"""
        self.unload_player()
        # Unload from noisemakers active loops
        del(self.nm.active_loops[self.loop_id])

if __name__ == '__main__':
    print "use launcher"
    sys.exit(1)
