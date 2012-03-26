#!/usr/bin/env python
import os,sys,math
import numpy as np
import matplotlib as mpl
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


        self.recalculate_normalizers()


        # These need to be one larger than the actual data
        mesh_x = np.arange(len(reactor.default_layout)+1) 
        mesh_y = np.arange(len(reactor.default_layout[0])+1) 
        self.X, self.Y = np.meshgrid(mesh_x,mesh_y)

        # figure dimensions
        self.fig_cols = 2
        self.fig_rows = int(math.ceil(float(len(self.temp_slices))/self.fig_cols))

        
        self.temp_fig, self.temps = plt.subplots(self.fig_rows, self.fig_cols)
        self.temp_fig.suptitle("Temparatures")

        # Set the data to axes
        for i in range(len(self.temp_slices)):
            row = i % self.fig_rows
            col = (i/self.fig_rows) % self.fig_cols
            # I hope these go as pointers cleanly
            self.temps[row][col].pcolor(self.X,self.Y,self.temp_slices[i], norm=self.temp_normalized)
            self.temps[row][col].set_title("Slice %d" % i)
        # Set the colorbar to the final space (which is empty for 7 slices)
        self.temp_cb = mpl.colorbar.ColorbarBase(self.temps[self.fig_rows-1][self.fig_cols-1], norm=self.temp_normalized, orientation='horizontal')
        self.temp_cb.set_label('Temperature')

        # Calculate how many reports we expec to receive before redraw, this is the number of rod/measurement wells
        self.reports_expected = 0
        for z in range(len(self.temp_slices)):
            for x in range(len(self.temp_slices[z])):
                for y in range(len(self.temp_slices[z][x])):
                    if reactor.default_layout[x][y] == ' ':
                        continue
                    self.reports_expected += 1
                    # initialize the well places to nonzero temp
                    self.temp_slices[z][x][y] = 22.0
                    
        # And recalculate the normalization again
        self.redraw()

        self.temp_reports_received = 0
        self.bus.add_signal_receiver(self.temp_report, dbus_interface = "fi.hacklab.reactorsimulator", signal_name = "emit_temp")
        self.neutron_reports_received = 0
        #self.bus.add_signal_receiver(self.neutron_report, dbus_interface = "fi.hacklab.reactorsimulator", signal_name = "emit_neutrons")

        plt.show()

    def recalculate_normalizers(self):
        self.max_temp = max(max(max(self.temp_slices)))
        self.temp_normalized = mpl.colors.Normalize(0.0, self.max_temp + 1.0)
    

    def redraw(self):
        self.recalculate_normalizers()

        # Set the data to axes
        for i in range(len(self.temp_slices)):
            row = i % self.fig_rows
            col = (i/self.fig_rows) % self.fig_cols
            # I hope these go as pointers cleanly
            self.temps[row][col].pcolor(self.X,self.Y,self.temp_slices[i], norm=self.temp_normalized)
            self.temps[row][col].set_title("Slice %d" % i)
        # Set the colorbar to the final space (which is empty for 7 slices)
        self.temp_cb = mpl.colorbar.ColorbarBase(self.temps[self.fig_rows-1][self.fig_cols-1], norm=self.temp_normalized, orientation='horizontal')
        self.temp_cb.set_label('Temperature')

        
        plt.draw()

    def temp_report(self, x, y, temp, sender):
        self.temp_reports_received += 1
        for i in range(len(temp)):
            self.temp_slices[i][x][y] = temp[i]
        if  (self.temp_reports_received % self.reports_expected == 0):
            self.redraw()

    def neutron_report(self, x, y, neutrons, sender):
        self.neutron_reports_received += 1
        for i in range(len(neutrons)):
            self.neutron_slices[i][x][y] = neutrons[i]
        if  (self.neutron_reports_received % self.reports_expected == 0):
            self.redraw()

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

