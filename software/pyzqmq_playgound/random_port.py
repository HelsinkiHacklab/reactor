#!/usr/bin/env python
import itertools
import random
import zmq
from zmq.eventloop import ioloop
ioloop.install()


import sys, os
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)
import zmq_utilities

service_name="test_pubsub"

@zmq_utilities.publish(service_name)
def test(arg1):
    pass

@zmq_utilities.publish(service_name)
def foo(arg1):
    pass

@zmq_utilities.publish(service_name)
def bar(arg1):
    pass

topic = itertools.cycle((test, foo, bar))

def send_random_data():
    data = "%s bottles of beer on the wall" % random.randint(0,100000)
    f = topic.next()
    f(data)

pcb = ioloop.PeriodicCallback(send_random_data, 100)
pcb.start()

ioloop.IOLoop.instance().start()
