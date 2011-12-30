# -*- coding: utf-8 -*-

"""Rod control panel"""

import sys

from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative


class Controller(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

    @QtCore.Slot(QtCore.QObject)
    def switch_changed(self, switch_instance):
        print "switch_changed called with id: %s, state: %s" % (switch_instance.property('id'), switch_instance.property('value'))

app = QtGui.QApplication(sys.argv)

view = QtDeclarative.QDeclarativeView()
view.setWindowTitle(__doc__)
view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

rc = view.rootContext()

controller = Controller()
rc.setContextProperty('controller', controller)

view.setSource(__file__.replace('.py', '.qml'))

view.show()
app.exec_()

