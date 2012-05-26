from __future__ import with_statement
# Boilerplate to add ../pythonlibs (via full path resolution) to import paths
import os,sys
libs_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', 'pythonlibs')
if os.path.isdir(libs_dir):                                       
    sys.path.append(libs_dir)

# Import our DBUS service module
import service,dbus,gobject,dbus_utilities
import dbus,time

class simcontrol(service.baseclass):
    def __init__(self, config, launcher_instance, **kwargs):
        super(simcontrol, self).__init__(config, launcher_instance, **kwargs)

    @dbus.service.method('fi.hacklab.reactorsimulator.simcontrol')
    def quit(self):
        return self.launcher_instance.quit()
