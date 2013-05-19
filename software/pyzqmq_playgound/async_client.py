#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()
import itertools
import random

import sys
myname = sys.argv[1]

import sys, os
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)
import bonjour_utilities


service_type="_zmqdealerrouter._tcp."
service_name="test_asyncrpc"


context = zmq.Context()
socket = context.socket(zmq.DEALER)

rr = bonjour_utilities.resolve(service_type, service_name)
connection_str =  "tcp://%s:%s" % (rr[1], rr[2])
print "connecting to %s" % connection_str
socket.connect(connection_str)

stream = ZMQStream(socket)


def client_recv_callback(*args):
    print "%s: client_recv_callback got %s" % (myname, repr(args))

stream.on_recv(client_recv_callback)

def send_random_data():
    data = "%d" % random.randint(0,100000)
    stream.send_multipart(("gimme", data))

pcb = ioloop.PeriodicCallback(send_random_data, 100)
pcb.start()


print "starting ioloop"
ioloop.IOLoop.instance().start()
