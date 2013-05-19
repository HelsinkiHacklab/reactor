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

def server_recv_callback(frames):
    print "server_recv_callback got %s" % repr(frames)
    command = None
    if len(frames) == 1:
        client_id = frames[0]
    if len(frames) > 2:
        client_id = frames[0]
        command = frames[1]
        data = frames[2:]
    if command:
        if command == "gimme":
            bottles = int(data[0])
            print "Sending bottles as reply"
            stream.send_multipart((client_id, "Here's %d bottles of beer" % bottles))
        else:
            print "Echoing data back to client"
            stream.send_multipart([client_id, command ] + list(data))


stream.on_recv(server_recv_callback)


print "starting ioloop"
ioloop.IOLoop.instance().start()
