# -*- coding: utf-8 -*-

"""Rod control panel"""

import sys, os

# Add arDuBUS path
# Don't do this yet, I have no dbus on my mac
#ardubus_module_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', '..', 'arDuBUS')
#if os.path.isdir(ardubus_module_dir):                                       
#    sys.path.append(ardubus_module_dir)
#import ardubus as ardubus_real
#
#class ardubus(ardubus_real.ardubus):
#    def __init__(self, bus, object_name):
#        # Fake config for now
#        import ConfigParser
#        config = ConfigParser.SafeConfigParser()
#        ardubus_real.ardubus.__init__(self, bus, object_name, config)
#
#    def initialize_serial(self):
#        print "Dummy serial"
#        pass


from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative


class Controller(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)


    @QtCore.Slot(QtCore.QObject)
    def switch_changed(self, switch_instance):
        # Switched to center
        if (int(switch_instance.property('value')) == 0):
            if (int(switch_instance.property('prevValue')) == 1):
                print "pin %d went high (ie switch stopped pulling down)" % int(switch_instance.property('upPin'))
            else:
                print "pin %d went high (ie switch stopped pulling down)" % int(switch_instance.property('downPin'))
            return
        # Switched up/down
        if (int(switch_instance.property('value')) == 1):
            print "pin %d went low" % int(switch_instance.property('upPin'))
        else:
            print "pin %d went low" % int(switch_instance.property('downPin'))
        return

class Proxy(QtCore.QObject):        
    def __init__(self, qml_root):
        QtCore.QObject.__init__(self)
        self.qml_root = qml_root

        # Start a timer to mess with the gauge
        timer = QtCore.QTimer(self)
        self.connect(timer, QtCore.SIGNAL("timeout()"), self.update_gauge)
        timer.start(2000)

    def update_gauge(self):
        import random
        self.qml_root.findChild(QtDeclarative.QDeclarativeItem, "servo1").setUSec(random.randint(1000,2000))
        #self.qml_root.findChild(QtDeclarative.QDeclarativeItem, "servo1").setPosition(random.randint(0,255))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle(__doc__)
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    
    rc = view.rootContext()


    controller = Controller()
    rc.setContextProperty('controller', controller)
    
    view.setSource(__file__.replace('.py', '.qml'))
    proxy = Proxy(view.rootObject())
    view.show()



    sys.exit(app.exec_())

