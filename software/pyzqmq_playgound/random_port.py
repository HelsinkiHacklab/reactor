#!/usr/bin/env python
import zmq
import itertools
import random

import pybonjour,socket

service_type="_zmqpubsub._tcp"
service_name="test_pubsub"

def bonjour_register_callback(sdRef,errorCode,name,regtype,domain):
	if errorCode == pybonjour.kDNSServiceErr_NoError:
		if name!=service_name or regtype != service_type:
			print "Something went wrong. service name or type don't match:",name,regtype
	else:
		print "Error",errorCode

context = zmq.Context()
socket = context.socket(zmq.PUB)
port_selected = socket.bind_to_random_port('tcp://*', min_port=49152, max_port=65535, max_tries=100)
print "Bound to %s" % repr(port_selected)

sdRef=pybonjour.DNSServiceRegister(service_name,service_type,port_selected,bonjour_register_callback)


topic = itertools.cycle(('test','foo','bar'))
while True:
	ready=socket.socket([sdRef],[],[])
	if sdRef in ready[0]:
		pybonjour.DNSServiceProcessResult(fd)
    data = "%s" % random.randint(0,100000)
    socket.send("%s %s" % (topic.next(), data))
