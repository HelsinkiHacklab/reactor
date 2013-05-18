#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

import itertools
import random
import pybonjour,socket

service_type="_zmqpubsub._tcp"
service_name="test_pubsub"
service_port=5555

def bonjour_register_callback(sdRef,errorCode,name,regtype,domain):
	if errorCode == pybonjour.kDNSServiceErr_NoError:
		if name!=service_name or regtype != service_type:
			print "Something went wrong. service name or type don't match:",name,regtype
	else:
		print "Error",errorCode

def bonjour_process_callback(fd,events):
	pybonjour.DNSServiceProcessResult(fd)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%d"%service_port)

sdRef=pybonjour.DNSServiceRegister(service_name,service_type,service_port,bonjour_register_callback)


topic = itertools.cycle(('test','foo','bar'))

stream = ZMQStream(socket)


def send_random_data():
    data = "%s bottles of beer on the wall" % random.randint(0,100000)
    stream.send_multipart((topic.next(), data))

pcb = ioloop.PeriodicCallback(send_random_data, 100)
pcb.start()

io_loop=ioloop.IOLoop.instance()

io_loop.add_handler(sdRef,bonjour_process_callback,io_loop.READ)
io_loop.start()
