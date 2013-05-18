#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, "test") # topic

stream = ZMQStream(socket)

def rec_callback(msg):
    print "received %s" % repr(msg)


stream.on_recv(rec_callback)

ioloop.IOLoop.instance().start()

