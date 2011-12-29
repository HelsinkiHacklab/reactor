# -*- coding: utf-8 -*-

"""Rod control panel"""

import sys

from PySide import QtCore
from PySide import QtGui
from PySide import QtDeclarative







app = QtGui.QApplication(sys.argv)

view = QtDeclarative.QDeclarativeView()
view.setWindowTitle(__doc__)
view.setResizeMode(QtDeclarative.QDeclarativeView.SizeRootObjectToView)

rc = view.rootContext()

#rc.setContextProperty('controller', controller)
#rc.setContextProperty('pythonListModel', zenItemList)
view.setSource(__file__.replace('.py', '.qml'))

view.show()
app.exec_()

