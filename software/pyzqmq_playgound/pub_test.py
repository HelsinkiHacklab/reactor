#!/usr/bin/env python
import zmq
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

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%d"%service_port)

sdRef=pybonjour.DNSServiceRegister(service_name,service_type,service_port,bonjour_register_callback)


topic = itertools.cycle(('test','foo','bar'))
while True:
	ready=socket.socket([sdRef],[],[])
	if sdRef in ready[0]:
		pybonjour.DNSServiceProcessResult(sdRef)
    data = "%s" % random.randint(0,100000)
    socket.send("%s %s" % (topic.next(), data))
