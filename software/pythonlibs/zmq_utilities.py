"""Utilities and decorators for PyZMQ"""
import zmq
from zmq.eventloop import ioloop
ioloop.install()
from zmq.eventloop.zmqstream import ZMQStream
import time
import bonjour_utilities
from functools import partial


def socket_type_to_service(socket_type):
    if socket_type == zmq.PUB:
        return "_zmqpubsub._tcp."
    if socket_type == zmq.SUB:
        return "_zmqpubsub._tcp."

    if socket_type == zmq.ROUTER:
        return "_zmqdealerrouter._tcp."
    if socket_type == zmq.DEALER:
        return "_zmqdealerrouter._tcp."

    # TODO: Implement more types
    # TODO: Raise error for unknown types


class zmq_client_response(object):
    client_id = None
    stream = None
    
    def __init__(self, client_id, stream):
        self.stream = stream
        self.client_id = client_id
    
    def send(self, *args):
        self.stream.send_multipart([self.client_id, ] + list(args))

class zmq_bonjour_bind_wrapper(object):
    context = None
    socket = None
    stream = None
    heartbeat_timer = None
    method_callbacks = {}


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

        if socket_type == zmq.PUB:
            # TODO: how to handle this with ROUTER/DEALER combinations...
            self.heartbeat_timer = ioloop.PeriodicCallback(self._hearbeat, 1000)
            self.heartbeat_timer.start()

        if socket_type == zmq.ROUTER:
            self.stream.on_recv(self._method_callback_wrapper)


        bonjour_utilities.register_ioloop(ioloop.IOLoop.instance(), service_type, service_name, service_port)

    def _method_callback_wrapper(self, datalist):
        #print "_method_callback_wrapper called: %s" % repr(datalist)
        if len(datalist) < 2:
            return
        client_id = datalist[0]
        method = datalist[1]
        args = datalist[2:]
        #print "DEBUG: _method_callback_wrapper(%s, %s)" % (method, repr(args))
        if not self.method_callbacks.has_key(method):
            print "No such method: %s" % method
            print "Methods: %s" % self.method_callbacks.keys()
            return
        for f in self.method_callbacks[method]:
            resp = zmq_client_response(client_id, self.stream)
            # TODO: make a wrapper object for sending responses and pass that instead of the client_id
            print "Calling f(resp, %s)" % repr(args)
            f(resp, *args)

    def register_method(self, name, callback):
        if not self.method_callbacks.has_key(name):
            self.method_callbacks[name] = []
        self.method_callbacks[name].append(callback)

class zmq_bonjour_connect_wrapper(object):
    context = None
    socket = None
    stream = None
    heartbeat_received = None
    heartbeat_timeout = 5000
    topic_callbacks = {}

    def __init__(self, socket_type, service_name, service_port=None, service_type=None):
        self.reconnect(socket_type, service_name, service_port=None, service_type=None)
        if socket_type == zmq.SUB:
            # TODO: how to handle this with ROUTER/DEALER combinations...
            self.add_topic_callback("HEARTBEAT", self._heartbeat_callback)
            # TODO: add heartbeat watcher callback

    def _heartbeat_callback(self, *args):
        self.heartbeat_received = time.time()
        #print "Heartbeat time %d" % self.heartbeat_received

    def _topic_callback_wrapper(self, datalist):
        topic = datalist[0]
        args = datalist[1:]
        #print "DEBUG: _topic_callback_wrapper(%s, %s)" % (topic, repr(args))
        if not self.topic_callbacks.has_key(topic):
            return
        for f in self.topic_callbacks[topic]:
            f(*args)

    def reconnect(self, socket_type, service_name, service_port=None, service_type=None):
        self.context = None
        self.socket = None
        self.stream = None
        self.heartbeat_received = None

        if not service_type:
            service_type = socket_type_to_service(socket_type)
        rr = bonjour_utilities.resolve(service_type, service_name)
        if not rr:
            # TODO raise error or wait ??
            return

        self.context = zmq.Context()
        self.socket = self.context.socket(socket_type)
        self.stream = ZMQStream(self.socket)
        connection_str =  "tcp://%s:%s" % (rr[1], rr[2])
        self.socket.connect(connection_str)

        # re-register the subscriptions
        for topic in self.topic_callbacks.keys():
            self._subscribe_topic(topic)

        # And set the callback
        self.stream.on_recv(self._topic_callback_wrapper)

    def _subscribe_topic(self, topic):
        self.socket.setsockopt(zmq.SUBSCRIBE, topic)

    def add_topic_callback(self, topic, callback):
        if not self.topic_callbacks.has_key(topic):
            self.topic_callbacks[topic] = []
            self._subscribe_topic(topic)
        self.topic_callbacks[topic].append(callback)

    



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

    def create(self, service_name, socket_type):
        service_type = service_type = socket_type_to_service(socket_type)
        key = "%s%s" % (service_name, service_type)
        self.by_names[key] = zmq_bonjour_bind_wrapper(socket_type, service_name)
        return self.by_names[key]

    def get_by_name_or_create(self, service_name, socket_type):
        r = self.get_by_name(service_name, socket_type)
        if not r:
            r = self.create(service_name, socket_type)
        return r

dt = decorator_tracker()

class signal(object):
    wrapper = None
    stream = None

    def __init__(self, service_name):
        self.wrapper = dt.get_by_name_or_create(service_name, zmq.PUB)
        self.stream = self.wrapper.stream

    def __call__(self, f):
        def wrapped_f(*args):
            topic = f.__name__
            self.stream.send_multipart([topic, ] + list(args))
            f(*args)
        return wrapped_f

class method(object):
    wrapper = None
    stream = None

    def __init__(self, service_name):
        print "Gettign wrapper"
        self.wrapper = dt.get_by_name_or_create(service_name, zmq.ROUTER)
        self.stream = self.wrapper.stream

    def __call__(self, f):
        method = f.__name__
        def wrapped_f(resp, *args):
            print "calling f(%s)" % repr(args)
            resp.send(f(*args))
        print "registering method %s" % method
        self.wrapper.register_method(method, wrapped_f)
        return wrapped_f


