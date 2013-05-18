#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

class GTK_Main():

    def __init__(self):
        self.player = gst.parse_launch('videotestsrc name=source ! video/x-raw-yuv,format=(fourcc)AYUV,width=500,height=400 ! videomixer name=mix ! ffmpegcolorspace !  autovideosink name=videosink')
        self.player.set_state(gst.STATE_PLAYING)


GTK_Main()
gtk.gdk.threads_init()
gtk.main()