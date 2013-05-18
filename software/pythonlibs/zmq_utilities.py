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


class zmq_bonjour(object):
    context = None
    socket = None
    stream = None

    def __init__(self, socket_type, service_name, service_port=None, service_type=None):
        self.context = zmq.Context()
        self.socket = self.context.socket(socket_type)
        if not service_port:
            service_port = self.socket.bind_to_random_port('tcp://*', min_port=49152, max_port=65535, max_tries=100)
        self.stream = stream = ZMQStream(self.socket)
        if not service_type:
            service_type = socket_type_to_service(socket_type)
        
        bonjour_utilities.register_ioloop(ioloop.IOLoop.instance(), service_type, service_name, service_port)

class decorator_tracker(object):
    by_names = {}

    def __init__(self):
        pass

    def get_by_name(self, service_name, socket_type):
        service_type = service_type = socket_type_to_service(socket_type)
        key = "%s%s" % (service_name, service_type)
        if self.by_names.has_key(key):
            return self.by_names[key]
        return None

    def get_by_name_or_create(self, service_name, socket_type):
        r = self.get_by_name(service_name, socket_type)
        if not r:
            service_type = service_type = socket_type_to_service(socket_type)
            key = "%s%s" % (service_name, service_type)
            self.by_names[key] = zmq_bonjour(socket_type, service_name)
            r = self.by_names[key]
        return r

dt = decorator_tracker()
