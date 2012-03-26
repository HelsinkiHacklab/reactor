#!/usr/bin/env python
import os,sys
import numpy as np
import matplotlib.pyplot as plt
import reactor

import dbus
import dbus.service

# Some links to matplotlib examples in case it desides to start giving "too many connections" errors to me again
#
# http://matplotlib.sourceforge.net/examples/pylab_examples/pcolor_demo.html
# http://matplotlib.sourceforge.net/examples/pylab_examples/image_nonuniform.html
# http://matplotlib.sourceforge.net/examples/pylab_examples/custom_cmap.html
# http://matplotlib.sourceforge.net/examples/axes_grid/demo_colorbar_with_inset_locator.html
# http://matplotlib.sourceforge.net/examples/pylab_examples/ellipse_collection.html


class reactor_listener():
    def __init__(self, bus, loop):
        self.bus = bus
        self.loop = loop
        

        self.temp_slices = [[[0.0 for z in range(reactor.default_depth)] for x in range(len(reactor.default_layout))] for y in range(len(reactor.default_layout[0]))]
        self.neutron_slices = [[[0.0 for z in range(reactor.default_depth)] for x in range(len(reactor.default_layout))] for y in range(len(reactor.default_layout[0]))]

        x = np.arange(len(reactor.default_layout))
        y = np.arange(len(reactor.default_layout[0]))
        X, Y = np.meshgrid(x,y)
        
        self.temp_fig, self.temps = plt.subplots(len(self.temp_slices), 1)
        

        
        self.bus.add_signal_receiver(self.temp_report, dbus_interface = "fi.hacklab.reactorsimulator", signal_name = "emit_temp")
        self.bus.add_signal_receiver(self.neutron_report, dbus_interface = "fi.hacklab.reactorsimulator", signal_name = "emit_neutrons")

        plt.show()

    def temp_report(self, x, y, temp, sender):
        for i in range(len(temp)):
            self.temp_slices[i][x][y] = temp[i]
        # redraw
        self.temps[0].canvas.draw()

    def neutron_report(self, x, y, neutrons, sender):
        for i in range(len(neutrons)):
            self.neutron_slices[i][x][y] = neutrons[i]
        # redraw
        self.neutrons[0].canvas.draw()

if __name__ == '__main__':
    import dbus.mainloop.glib, gobject
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    
    bus = dbus.SessionBus()
    loop = gobject.MainLoop()
    listener = reactor_listener(bus, loop)


    # TODO: Add some nicer way to exit than ctrl-c
    listener.loop.run()

