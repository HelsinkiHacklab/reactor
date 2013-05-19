#!/usr/bin/env python

import sys, os
import pygtk, gtk, gobject
import pygst
pygst.require("0.10")
import gst

import sys, os
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):
    sys.path.append(libs_dir)
import framebuffer_info

width, height = framebuffer_info.resolution()

class GTK_Main():

    def __init__(self):
#        launch_str = 'videotestsrc name=source ! video/x-raw-yuv,format=(fourcc)AYUV,width=%d,height=%d ! videomixer name=mix ! ffmpegcolorspace !  fbdevsink name=videosink' % (width, height)
        launch_str = 'videotestsrc name=source ! video/x-raw-rgb,width=%d,height=%d ! ffmpegcolorspace !  fbdevsink name=videosink' % (width, height)
        print "Calling gst.parse_launch('%s')" % launch_str
        self.player = gst.parse_launch(launch_str)
        self.player.set_state(gst.STATE_PLAYING)


GTK_Main()
gtk.gdk.threads_init()
gtk.main()