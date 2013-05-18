#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

import itertools
import random


import sys, os
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)
import bonjour_utilities


service_type="_zmqpubsub._tcp."
service_name="test_pubsub"

context = zmq.Context()
socket = context.socket(zmq.PUB)
port_selected = socket.bind_to_random_port('tcp://*', min_port=49152, max_port=65535, max_tries=100)
print "Bound to %s" % repr(port_selected)

topic = itertools.cycle(('test','foo','bar'))
stream = ZMQStream(socket)

def send_random_data():
    data = "%s bottles of beer on the wall" % random.randint(0,100000)
    stream.send_multipart((topic.next(), data))

pcb = ioloop.PeriodicCallback(send_random_data, 100)
pcb.start()

io_loop=ioloop.IOLoop.instance()

bonjour_utilities.register_ioloop(io_loop, service_type, service_name, port_selected)

io_loop.start()
