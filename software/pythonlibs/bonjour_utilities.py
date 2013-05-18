"""utilities built on pybonjour"""
import pybonjour, select

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

resolver = bonjour_resolver()

def resolve(service_type, service_name=None):
    return resolver.resolve(service_type, service_name)
