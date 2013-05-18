#!/usr/bin/env python
import zmq
from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
ioloop.install()

import sys, os
import pybonjour

class bonjour_resolver(object):
    resolved = None
    name_filter = None
    resolve_error = False
    timeout = 5
    
    def __init__(self):
        pass

    def resolve(self, service_type, service_name=None):
        import select
        self.name_filter = service_name
        self.resolve_error = False
        browse_sdRef = pybonjour.DNSServiceBrowse(regtype = service_type, callBack = self._browse_callback)

        try:
            while True:
                ready = select.select([browse_sdRef], [], [])
                if browse_sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(browse_sdRef)
    
                if (   self.resolve_error
                    or self.resolved):
                        break
        finally:
            browse_sdRef.close()        

        if self.resolved:
            return self.resolved
        
        return False

    def _resolve_callback(self, sdRef, flags, interfaceIndex, errorCode, fullname, hosttarget, port, txtRecord):
        print "_resolve_callback called"
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return
        self.resolved = (fullname, hosttarget, port)
    
    def _browse_callback(self, sdRef, flags, interfaceIndex, errorCode, serviceName, regtype, replyDomain):
        print "_browse_callback called"
        import select
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return
        if not (flags & pybonjour.kDNSServiceFlagsAdd):
            return

        if (    self.name_filter
            and serviceName != self.name_filter):
            print "Found service '%s' but it does not match '%s'" % (serviceName, self.name_filter)
            return 

        resolve_sdRef = pybonjour.DNSServiceResolve(
            0,
            interfaceIndex,
            serviceName,
            regtype,
            replyDomain,
            self._resolve_callback
        )

        try:
            while not self.resolved:
                ready = select.select([resolve_sdRef], [], [], self.timeout)
                if resolve_sdRef not in ready[0]:
                    print 'Resolve timed out'
                    self.resolve_error = True
                    break
                pybonjour.DNSServiceProcessResult(resolve_sdRef)
        finally:
            resolve_sdRef.close()

r = bonjour_resolver()
rr = r.resolve("_zmqpubsub._tcp.")
if not rr:
    print "Could not find service"
    sys.exit(1)

connection_str =  "tcp://%s:%s" % (rr[1], rr[2])
print "Connecting to %s" % connection_str

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect(connection_str)
socket.setsockopt(zmq.SUBSCRIBE, "test") # subscribe to topic
socket.setsockopt(zmq.SUBSCRIBE, "bar") # subscribe to another topic

stream = ZMQStream(socket)

def rec_callback(msg):
    topic, data = msg
    print "received %s: %s" % (topic, data)

stream.on_recv(rec_callback)

print "starting ioloop"
ioloop.IOLoop.instance().start()

