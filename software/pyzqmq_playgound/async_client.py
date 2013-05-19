#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()
import itertools
import random


service_type="_zmqdealerrouter._tcp."
service_name="test_asyncrpc"
service_port=5556


context = zmq.Context()
socket = context.socket(zmq.DEALER)
socket.connect("tcp://*:%d"%service_port)
stream = ZMQStream(socket)


def client_recv_callback(*args):
    print "client_recv_callback got %s" % repr(args)

stream.on_recv(client_recv_callback)

def send_random_data():
    data = "%d" % random.randint(0,100000)
    stream.send_multipart(("gimme", data))

pcb = ioloop.PeriodicCallback(send_random_data, 100)
pcb.start()


print "starting ioloop"
ioloop.IOLoop.instance().start()
