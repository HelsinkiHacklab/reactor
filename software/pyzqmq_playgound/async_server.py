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


service_name="test_asyncrpc"

wrapper = zmq_utilities.zmq_bonjour_bind_wrapper(zmq.ROUTER, service_name)
stream = wrapper.stream

def beer(resp, bottles):
    bottles = int(bottles)
    print "Sending bottles as reply"
    resp.send("Here's %d bottles of beer" % bottles)

def food(resp, arg):
    print "Sending noms as reply"
    resp.send("Here's %s for the noms" % arg)

wrapper.register_method("gimme", beer)
wrapper.register_method("nom", food)


print "starting ioloop"
ioloop.IOLoop.instance().start()
