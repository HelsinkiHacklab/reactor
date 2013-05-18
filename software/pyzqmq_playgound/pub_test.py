#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

import itertools
import random
import pybonjour,socket
from functools import partial

service_type="_zmqpubsub._tcp."
service_name="test_pubsub"
service_port=5555

def bonjour_register_callback(sdRef, flags, errorCode, name, regtype, domain):
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        if name!=service_name or regtype != service_type:
            print "Something went wrong. service name or type don't match: '%s' =! '%s' or '%s' != '%s'" % (name, service_name , regtype, service_type)
    else:
        print "Error",errorCode

def bonjour_process_callback(fd, events, sdRef=None):
    pybonjour.DNSServiceProcessResult(sdRef)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%d"%service_port)

sdRef=pybonjour.DNSServiceRegister(name=service_name,regtype=service_type,port=service_port,callBack=bonjour_register_callback)


topic = itertools.cycle(('test','foo','bar'))

stream = ZMQStream(socket)


def send_random_data():
    data = "%s bottles of beer on the wall" % random.randint(0,100000)
    stream.send_multipart((topic.next(), data))

pcb = ioloop.PeriodicCallback(send_random_data, 100)
pcb.start()

io_loop=ioloop.IOLoop.instance()

bonjour_process_callback_sdref = partial(bonjour_process_callback, sdRef = sdRef)
io_loop.add_handler(sdRef.fileno(),bonjour_process_callback_sdref,io_loop.READ)
io_loop.start()
