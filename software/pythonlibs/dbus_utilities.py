"""Some utility functions to hve more grafull handling of DBUS exceptions we might get when dependent services get restarted"""
import dbus

dbus_cache = {}
dbus_cache_error_count = {}
bus = dbus.SessionBus()

def call_cached(buspath, method, *args, **kwargs):
    """Maintains a cache of DBUS proxy objects and calls the given objects method. If the proxy object is stale tries to refresh"""
    if not kwargs.has_key('busname'):
        kwargs['busname'] = buspath.replace('/', '.')[1:]
    busname = kwargs['busname']
    obj_cache_key = "%s@%s" % (busname, buspath)
    method_cache_key = "%s::%s" % (obj_cache_key, method)
    if not dbus_cache.has_key(obj_cache_key):
        dbus_cache[obj_cache_key] = bus.get_object(busname, buspath)
    if not dbus_cache.has_key(method_cache_key):
        dbus_cache[method_cache_key] = getattr(dbus_cache[obj_cache_key], method)

    try:
        ret = dbus_cache[method_cache_key](*args)
        if dbus_cache_error_count.has_key(method_cache_key): # Zero the error count
            dbus_cache_error_count[method_cache_key] = 0
        return ret                
    except dbus.exceptions.DBusException:
        if not dbus_cache_error_count.has_key(method_cache_key):
            dbus_cache_error_count[method_cache_key] = 0
        dbus_cache_error_count[method_cache_key] += 1
        # TODO Check that it's a method os object name exception first
        # Remove stale keys
        print "dbus_utilities.call_cached: Removing stale keys for %s" % method_cache_key
        del(dbus_cache[obj_cache_key])
        del(dbus_cache[method_cache_key])
        if dbus_cache_error_count[method_cache_key] < 4:
            return call_cached(busname, buspath, method, *args)
