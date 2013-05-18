"""utilities built on pybonjour"""
import pybonjour, select
from functools import partial

class bonjour_resolver(object):
    resolved = None
    name_filter = None
    resolve_error = False
    timeout = 5
    
    def __init__(self):
        pass

    def resolve(self, service_type, service_name=None):
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
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return
        self.resolved = (fullname, hosttarget, port)
    
    def _browse_callback(self, sdRef, flags, interfaceIndex, errorCode, serviceName, regtype, replyDomain):
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

# Shorthand for the resolver
resolver = bonjour_resolver()
def resolve(service_type, service_name=None):
    return resolver.resolve(service_type, service_name)

class bonjour_registrar(object):
    registered = None
    register_error = False
    timeout = 5

    def _register_callback(self, sdRef, flags, errorCode, name, regtype, domain):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            print "Registered service", name,regtype,domain
            self.registered = (name, regtype, domain)
        else:
            print "Error",errorCode
            self.register_error = True

    def _process_callback(self, fd, events, sdRef=None):
        pybonjour.DNSServiceProcessResult(sdRef)

    def register_ioloop(self, io_loop, service_type, service_name, service_port):
        sdRef=pybonjour.DNSServiceRegister(name=service_name, regtype=service_type, port=service_port, callBack=self._register_callback)
        process_callback_sdref = partial(self._process_callback, sdRef = sdRef)
        io_loop.add_handler(sdRef.fileno(), process_callback_sdref, io_loop.READ)
        
        return self.registered


# Shorthand for the registrar
registrar = bonjour_registrar()
def register_ioloop(io_loop, service_type, service_name, service_port):
    return registrar.register_ioloop(io_loop, service_type, service_name, service_port)
