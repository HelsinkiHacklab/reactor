# ardubus simulator
from Tkinter import *
import sys, os
import ConfigParser
import ardubus
import dbus

def quit_callback():
    sys.exit(0)

class PinButton():
    def cb(self):
        self.abus.dio_change(self.pin, self.var.get(), self.name)
    
    def __init__(self, root, abus, name, pin, row, col):
        self.name = name
        self.abus = abus
        self.pin = pin
        self.var = IntVar()
        Checkbutton(root, variable=self.var, command=lambda: self.cb()).grid(row=row, column=col)
    
class Simu():
    def init_toolbar(self):
        self.toolbar = Frame(self.root)
        b = Button(self.toolbar, text="Quit", width=6, command=quit_callback)
        b.pack(side=LEFT, padx=2, pady=2)
        self.toolbar.grid(row=self.row)
        self.row += 1

    def make_board(self, name, row):
        abus = ardubus.ardubus(self.bus, name, self.config)
        Label(self.root, text=name).grid(row=row)
        for i in range(0,42):
            PinButton(self.root, abus, name, i, row, i+1)

    def init_boards(self):
        for board_name in self.config.sections():
            self.make_board(board_name, self.row)
            self.row += 1

    def init_bus(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SessionBus()

    def __init__(self, config):
        self.root = Tk()
        self.config = config
        self.row = 0

        self.init_bus()
        self.init_toolbar()

        for i in range(0, 42):
            Label(self.root, text=str(i)).grid(row=self.row, column=i+1)
        self.row += 1
        self.init_boards()
    
    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    config = ConfigParser.SafeConfigParser()
    if not os.path.isfile('ardubus.conf'):
        config.add_section('arduino0')
        config.set('arduino0', 'device', '/dev/ttyUSB0')

        config.add_section('arduino1')
        config.set('arduino1', 'device', '/dev/ttyUSB1')
        
        # TODO: Other defaults
        with open('ardubus.conf', 'wb') as configfile:
            config.write(configfile)
    config.read('ardubus.conf')
    
    s = Simu(config)
    s.run()
    
    
