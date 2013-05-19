#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

service_type="_zmqdealerrouter._tcp."
service_name="test_asyncrpc"
service_port=5556


context = zmq.Context()
socket = context.socket(zmq.ROUTER)
socket.bind("tcp://*:%d"%service_port)
stream = ZMQStream(socket)

def server_recv_callback(*args):
    print "recv_callback got %s" % repr(args)


stream.on_recv(server_recv_callback)


print "starting ioloop"
ioloop.IOLoop.instance().start()
