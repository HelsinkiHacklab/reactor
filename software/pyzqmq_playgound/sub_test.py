#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

port = 5555
import sys
if len(sys.argv) > 1:
    port = int(sys.argv[1])

context = zmq.Context()
socket = context.socket(zmq.SUB)
print "Connecting to tcp://localhost:%s" % port
socket.connect("tcp://localhost:%s" % port)
socket.setsockopt(zmq.SUBSCRIBE, "test") # topic

stream = ZMQStream(socket)

def rec_callback(msg):
    print "received %s" % repr(msg)


stream.on_recv(rec_callback)

ioloop.IOLoop.instance().start()

