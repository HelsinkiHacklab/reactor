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


import itertools
import random

service_type="_zmqpubsub._tcp."
service_name="test_pubsub"
service_port=5555


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%d"%service_port)

io_loop=ioloop.IOLoop.instance()
bonjour_utilities.register_ioloop(io_loop, service_type, service_name, service_port)

topic = itertools.cycle(('test','foo','bar'))
stream = ZMQStream(socket)

def send_random_data():
    data = "%s bottles of beer on the wall" % random.randint(0,100000)
    #socket.send_multipart((topic.next(), data))
    stream.send_multipart((topic.next(), data))

pcb = ioloop.PeriodicCallback(send_random_data, 100)
pcb.start()




io_loop.start()
