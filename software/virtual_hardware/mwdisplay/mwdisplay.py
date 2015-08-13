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
    def __init__(self, view, bus):
        QtCore.QObject.__init__(self)
        self.view = view
        self.bus = bus

        self.bus.add_signal_receiver(self.power_report, dbus_interface = 'fi.hacklab.reactorsimulator.engine', signal_name = "emit_power")


    def power_report(self, power, *args):
        self.view.rootObject().findChild(QtDeclarative.QDeclarativeItem, 'mwtext').setText("%d MW" % int(power))


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
    mwdisplay = MWDisplay(view, bus)
    rc.setContextProperty('MW', mwdisplay)
    
    view.setSource(__file__.replace('.py', '.qml'))
    view.show()
    
    sys.exit(app.exec_())

