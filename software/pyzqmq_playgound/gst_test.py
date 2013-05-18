#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

# These are from /boot/config.txt
overscan_left=30
overscan_right=10
overscan_top=0
overscan_bottom=0

width=640-overscan_left-overscan_right
height=420-overscan_top-overscan_bottom


class GTK_Main():

    def __init__(self):
        launch_str = 'videotestsrc name=source ! video/x-raw-yuv,format=(fourcc)AYUV,width=%d,height=%d ! videomixer name=mix ! ffmpegcolorspace !  fbdevsink name=videosink' % (width, height)
        print "Calling gst.parse_launch('%s')" % launch_str
        self.player = gst.parse_launch(launch_str)
        self.player.set_state(gst.STATE_PLAYING)


GTK_Main()
gtk.gdk.threads_init()
gtk.main()