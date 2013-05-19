#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

import sys, os
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)
import bonjour_utilities


rr = bonjour_utilities.resolve("_zmqpubsub._tcp.", "test_pubsub")
if not rr:
    print "Could not find service"
    sys.exit(1)

connection_str =  "tcp://%s:%s" % (rr[1], rr[2])
print "Connecting to %s" % connection_str

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(connection_str)
socket.setsockopt(zmq.SUBSCRIBE, "HEARTBEAT") # subscribe to topic
socket.setsockopt(zmq.SUBSCRIBE, "test") # subscribe to topic
socket.setsockopt(zmq.SUBSCRIBE, "bar") # subscribe to another topic

stream = ZMQStream(socket)

def rec_callback(msg):
    topic, data = msg
    print "received %s: %s" % (topic, data)

stream.on_recv(rec_callback)

print "starting ioloop"
ioloop.IOLoop.instance().start()

