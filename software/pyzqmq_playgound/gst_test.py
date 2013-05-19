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
try:
    import framebuffer_info
    width, height = framebuffer_info.resolution()
except:
    # These are from /boot/config.txt
    overscan_left=30
    overscan_right=10
    overscan_top=0
    overscan_bottom=0
    
    width=560+overscan_left+overscan_right
    height=420+overscan_top+overscan_bottom
    


#videos_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', '..', 'videos')
videos_dir = '/home/pi/test_videos'
path = os.path.join(videos_dir, "rammstein-ich_will.mp4")

# kts http://www.raspberrypi.org/phpBB3/viewtopic.php?f=38&t=19606
videosink = "autovideosink"
#videosink = "fbdevsink"
#audiosink = "autoaudiosink"
audiosink = "alsasink"
#audiosink = "alsasink device=hw:0,0 sync=false"


class GTK_Main():
    playmode = False

    def __init__(self):
#        launch_str = 'videotestsrc name=source ! video/x-raw-yuv,format=(fourcc)AYUV,width=%d,height=%d ! videomixer name=mix ! ffmpegcolorspace !  fbdevsink name=videosink' % (width, height)
        # These two work
#        launch_str = 'videotestsrc name=source ! video/x-raw-rgb,width=%d,height=%d ! ffmpegcolorspace !  fbdevsink name=videosink' % (width, height)
#        launch_str = 'videotestsrc name=source ! video/x-raw-rgb,width=%d,height=%d ! ffmpegcolorspace !  %s name=videosink' % (width, height, videosink)
        # This works
#        launch_str = 'audiotestsrc name=audiosource ! audioconvert ! %s name=audiosink' % (audiosink)

        # Fail ?
#        launch_str = "filesrc name=filesource ! decodebin name=decode decode. ! videoscale ! video/x-raw-rgb,width=%d,height=%d ! ffmpegcolorspace ! %s name=videosink decode. ! audioconvert ! %s " % (width, height, videosink, audiosink)
#        launch_str = "filesrc name=filesource ! decodebin name=decode decode. ! videoscale ! ffmpegcolorspace ! %s name=videosink decode. ! audioconvert ! %s " % (videosink, audiosink)
        # This works with X11 on my linux VM but not on the raspberry...
        launch_str = "filesrc location=%s ! decodebin name=decode decode. ! videoscale ! ffmpegcolorspace ! %s name=videosink decode. ! audioconvert ! %s " % (path, videosink, audiosink)
        print "Calling gst.parse_launch('%s')" % launch_str

        self.player = gst.parse_launch(launch_str)
        vbus = self.player.get_bus()
        vbus.add_signal_watch()
        vbus.connect("message", self.on_message)


        filesrcelem = self.player.get_by_name("filesource")
        if filesrcelem:
            print "Setting file to %s" % path
            filesrcelem.set_property("location", path)
        print "Pressing PLAY"
        self.player.set_state(gst.STATE_PLAYING)
        self.playmode = True

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            print "MESSAGE_EOS"
            self.player.set_state(gst.STATE_NULL)
            self.playmode = False
        elif t == gst.MESSAGE_ERROR:
            print "MESSAGE_ERROR"
            self.player.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.playmode = False


GTK_Main()
gtk.gdk.threads_init()
gtk.main()