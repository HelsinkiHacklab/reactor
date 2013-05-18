#!/usr/bin/env python
import zmq
import itertools
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

topic = itertools.cycle(('test','foo','bar'))
while True:
    data = "%s" % random.randint(0,100000)
    socket.send_multipart((topic.next(), data))
