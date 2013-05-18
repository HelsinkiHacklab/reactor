#!/usr/bin/env python
import zmq

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")

socket.setsockopt(zmq.SUBSCRIBE, "test") # topic

while True:
    recv = socket.recv()
    topic, data = recv.split(' ',1)
    print "received %s: %s" % (topic, data)
