#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

import sys, os
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)
import zmq_utilities


wrapper = zmq_utilities.zmq_bonjour_connect_wrapper(zmq.SUB, "test_pubsub")

def test_callback(data):
    print "in test_callback got %s" % repr(data)

def test_callback2(data):
    print "in test_callback2 got %s" % repr(data)


def bar_callback(data):
    print "in bar_callback got %s" % repr(data)

wrapper.add_topic_callback("test", test_callback)
wrapper.add_topic_callback("bar", bar_callback)
wrapper.add_topic_callback("test", test_callback2)

print "starting ioloop"
ioloop.IOLoop.instance().start()

