"""Utilities and decorators for PyZMQ"""
import zmq
from zmq.eventloop import ioloop
ioloop.install()
from zmq.eventloop.zmqstream import ZMQStream

import bonjour_utilities

def socket_type_to_service(socket_type):
    if socket_type == zmq.PUB:
        return "_zmqpubsub._tcp."
    if socket_type == zmq.SUB:
        return "_zmqpubsub._tcp."

    # TODO: Implement more types
    # TODO: Raise error for unknown types


class zmq_bonjour_wrapper(object):
    context = None
    socket = None
    stream = None
    heartbeat_timer = None

    def _hearbeat(self):
        #print "Sending heartbeat"
        self.stream.send_multipart(("HEARTBEAT", "1"))

    def __init__(self, socket_type, service_name, service_port=None, service_type=None):
        self.context = zmq.Context()
        self.socket = self.context.socket(socket_type)
        if not service_port:
            service_port = self.socket.bind_to_random_port('tcp://*', min_port=49152, max_port=65535, max_tries=100)
        else:
            self.socket.bind("tcp://*:%d" % service_port)
        print "Bound to port %d" % service_port

        self.stream = ZMQStream(self.socket)
        if not service_type:
            service_type = socket_type_to_service(socket_type)

        
        self.heartbeat_timer = ioloop.PeriodicCallback(self._hearbeat, 1000)
        self.heartbeat_timer.start()

        bonjour_utilities.register_ioloop(ioloop.IOLoop.instance(), service_type, service_name, service_port)


class decorator_tracker(object):
    by_names = {}

    def __init__(self):
        pass

    def get_by_name(self, service_name, socket_type):
        service_type = socket_type_to_service(socket_type)
        key = "%s%s" % (service_name, service_type)
        if self.by_names.has_key(key):
            return self.by_names[key]
        return None

    def get_by_name_or_create(self, service_name, socket_type):
        r = self.get_by_name(service_name, socket_type)
        if not r:
            service_type = service_type = socket_type_to_service(socket_type)
            key = "%s%s" % (service_name, service_type)
            self.by_names[key] = zmq_bonjour_wrapper(socket_type, service_name)
            r = self.by_names[key]
        return r

dt = decorator_tracker()

class publish(object):
    wrapper = None
    stream = None

    def __init__(self, service_name):
        self.wrapper = dt.get_by_name_or_create(service_name, zmq.PUB)
        self.stream = self.wrapper.stream

    def __call__(self, f):
        def wrapped_f(*args):
            topic = f.__name__
            self.stream.send_multipart(topic, *args)
            f(*args)
        return wrapped_f