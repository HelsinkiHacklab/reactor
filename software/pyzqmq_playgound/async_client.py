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
import zmq_utilities

service_name="test_asyncrpc"

#wrapper = zmq_utilities.ct.get_by_name_or_create(service_name, zmq.DEALER)
wrapper = zmq_utilities.zmq_bonjour_connect_wrapper(zmq.DEALER, service_name)

stream = wrapper.stream

def client_recv_callback(*args):
    print "%s: client_recv_callback got %s" % (myname, repr(args))

stream.on_recv(client_recv_callback)

def send_random_data():
    data = "%d" % random.randint(0,100000)
    #zmq_utilities.call(service_name, "beer", data)
    zmq_utilities.call(wrapper, "beer", data)
    if random.randint(0,1):
        #zmq_utilities.call(service_name, "food", data)
        zmq_utilities.call(wrapper, "food", data)
        

pcb = ioloop.PeriodicCallback(send_random_data, 100)
pcb.start()


print "starting ioloop"
ioloop.IOLoop.instance().start()
