#!/usr/bin/env python
import zmq
import itertools
import random

context = zmq.Context()
socket = context.socket(zmq.PUB)
port_selected = socket.bind_to_random_port('tcp://*', min_port=49152, max_port=65535, max_tries=100)
print "Bound to %s" % repr(port_selected)

topic = itertools.cycle(('test','foo','bar'))
while True:
    data = "%s" % random.randint(0,100000)
    socket.send("%s %s" % (topic.next(), data))
