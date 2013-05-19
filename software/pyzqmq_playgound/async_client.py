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


def recv_callback(client_id, command, *args):
    print "recv_callback got %s" % repr(args)
    if command == "gimme":
        bottles = args[0]
        stream.send_multipart((client_id, "Here's %d bottles of beer" % bottles))
    else:
        stream.send_multipart([client_id, ] + list(args))
    


stream.on_recv(recv_callback)

def send_random_data():
    data = "%s" % random.randint(0,100000)
    stream.send_multipart(("gimme", data))

pcb = ioloop.PeriodicCallback(send_random_data, 100)
pcb.start()


print "starting ioloop"
ioloop.IOLoop.instance().start()
