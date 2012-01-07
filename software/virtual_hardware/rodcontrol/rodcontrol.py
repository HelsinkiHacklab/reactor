# -*- coding: utf-8 -*-

"""Rod control panel"""

import sys, os

ardubus_module_dir = os.path.join(os.path.dirname( os.path.realpath( __file__ ) ),  '..', '..', 'arDuBUS')
if os.path.isdir(ardubus_module_dir):                                       
    sys.path.append(ardubus_module_dir)
import ardubus_qml as ardubus
import dbus
import dbus.service
import dbus.mainloop.glib

# Use a global for storing these
ardubus_instances = {}


from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative


class Controller(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)


    @QtCore.Slot(QtCore.QObject)
    def switch_changed(self, switch_instance):
        ardubus_proxy = ardubus_instances[switch_instance.property('boardName')]
        # Switched to center
        if (int(switch_instance.property('value')) == 0):
            if (int(switch_instance.property('prevValue')) == 1):
                print "pin %d went high (ie switch stopped pulling down)" % int(switch_instance.property('upPin'))
                ardubus_proxy.dio_change(switch_instance.property('upPin'), True, ardubus_proxy.object_name)
            else:
                print "pin %d went high (ie switch stopped pulling down)" % int(switch_instance.property('downPin'))
                ardubus_proxy.dio_change(switch_instance.property('downPin'), True, ardubus_proxy.object_name)
            return
        # Switched up/down
        if (int(switch_instance.property('value')) == 1):
            print "pin %d went low" % int(switch_instance.property('upPin'))
            ardubus_proxy.dio_change(switch_instance.property('upPin'), False, ardubus_proxy.object_name)
        else:
            print "pin %d went low" % int(switch_instance.property('downPin'))
            ardubus_proxy.dio_change(switch_instance.property('downPin'), False, ardubus_proxy.object_name)
        return

class QMLProxy(QtCore.QObject):        
    def __init__(self, qml_root):
        QtCore.QObject.__init__(self)
        self.qml_root = qml_root


    def get_object(self, objectName):
        return self.qml_root.findChild(QtDeclarative.QDeclarativeItem, objectName)

if __name__ == '__main__':
    # not using threading yet, besided I think I should use QT threads anyway
    #gobject.threads_init()
    #dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()



    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle(__doc__)
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    
    rc = view.rootContext()
    controller = Controller()
    rc.setContextProperty('controller', controller)
    
    view.setSource(__file__.replace('.py', '.qml'))
    proxy = QMLProxy(view.rootObject())
    view.show()
    
    servo_arduino = ardubus.ardubus_qml(bus, 'arduino0', proxy)
    ardubus_instances[servo_arduino.object_name] = servo_arduino
    switch_arduino = ardubus.ardubus_qml(bus, 'arduino1', proxy)
    ardubus_instances[switch_arduino.object_name] = switch_arduino



    sys.exit(app.exec_())

