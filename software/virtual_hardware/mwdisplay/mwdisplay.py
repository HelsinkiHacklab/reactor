# -*- coding: utf-8 -*-

import sys, os

# import python dbus module
import dbus
# import python dbus GLib mainloop support
import dbus.mainloop.glib
# import QtCore
from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative


class MWDisplay(QtCore.QObject):
    def __init__(self, bus):
        QtCore.QObject.__init__(self)
        self.bus = bus

if __name__ == '__main__':
    # Yes we are using threads, in ardubus_qml.py....
    import gobject,dbus.mainloop.glib
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()

    app = QtGui.QApplication(sys.argv)
    view = QtDeclarative.QDeclarativeView()
    view.setWindowTitle(__doc__)
    view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)
    
    rc = view.rootContext()
    mwdisplay = MWDisplay(bus)
    rc.setContextProperty('MW', mwdisplay)
    
    view.setSource(__file__.replace('.py', '.qml'))
    proxy = QMLProxy(view.rootObject())
    view.show()
    
    sys.exit(app.exec_())

