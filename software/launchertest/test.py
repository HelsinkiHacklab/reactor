# Boilerplate to add ../pythonlibs (via full path resolution) to import paths
import os,sys
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)

# Import our DBUS service module
import service

class test(service.baseclass):
    def __init__(self, mainloop, bus, config, **kwargs):
        super(test, self).__init__(mainloop, bus, config, **kwargs)
        print "launcher test mainclass initialized as %s:%s with config %s" % (self.dbus_interface_name, self.dbus_object_path, repr(self.config))

