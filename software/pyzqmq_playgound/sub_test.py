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

wrapper.socket.setsockopt(zmq.SUBSCRIBE, "HEARTBEAT") # subscribe to topic
wrapper.socket.setsockopt(zmq.SUBSCRIBE, "test") # subscribe to topic
wrapper.socket.setsockopt(zmq.SUBSCRIBE, "bar") # subscribe to another topic


def rec_callback(msg):
    topic, data = msg
    print "received %s: %s" % (topic, data)

wrapper.stream.on_recv(rec_callback)

print "starting ioloop"
ioloop.IOLoop.instance().start()

