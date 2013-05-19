#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

# Insert code here


print "starting ioloop"
ioloop.IOLoop.instance().start()
