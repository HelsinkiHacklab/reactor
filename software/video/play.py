#!/usr/bin/env python

import sys, os, time, thread
import glib, gobject
import dbus
import dbus.service
import dbus.mainloop.glib
import pygst
pygst.require("0.10")
import gst
import ConfigParser
#import pygtk, gtk 

class videoplay_listener():
	
    def __init__(self, bus, config):
        #self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #self.win.set_default_size(800, 600)
        #self.win.set_default_pos(0,0)
        #vbox = gtk.VBox()
        #self.win.add(vbox)

        self.player = gst.parse_launch("filesrc name=source ! decodebin name=decode decode. ! ffmpegcolorspace ! autovideosink decode. ! audioconvert ! autoaudiosink")
        vbus = self.player.get_bus()
        vbus.add_signal_watch()
        vbus.connect("message", self.on_message)
        
        self.videos = {} 

        for video in config.items('videos'):
            print "setting video file", video[1], "for signal event_video('%s')" % video[0]
            self.videos[video[0]] = video[1]

        bus.add_signal_receiver(self.play_video, dbus_interface = "fi.hacklab.ardubus", 
                                signal_name = 'event_video')
        #self.win.show_all()

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            self.playmode = False
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.playmode = False
 
    def play_video(self, name):
        thread.start_new_thread(self.play_it, (self.videos[name],))

    def play_it(self, path):
        self.playmode = True
        self.player.get_by_name("source").set_property("location", path)
        self.player.set_state(gst.STATE_PLAYING)
        while self.playmode:
            time.sleep(1)
        self.player = gst.parse_launch("filesrc name=source ! decodebin name=decode decode. ! ffmpegcolorspace ! autovideosink decode. ! audioconvert ! autoaudiosink")
        vbus = self.player.get_bus()
        vbus.add_signal_watch()
        vbus.connect("message", self.on_message)
#        self.player.set_state(gst.STATE_NULL)

if __name__ == '__main__':
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    config = ConfigParser.SafeConfigParser()
    config.read("videos.cfg")

    bus = dbus.SessionBus()
    videoconsole = videoplay_listener(bus, config)
    #gtk.gdk.threads_init()
    #gtk.main()
    loop = gobject.MainLoop()
    loop.run()

