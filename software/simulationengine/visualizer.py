#!/usr/bin/env python
from __future__ import with_statement
import os,sys,time
import math
import numpy as np
import matplotlib as mpl
mpl.use('GTKAgg')  # or 'GTK'
import matplotlib.pyplot as plt
import reactor
import gtk
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.figure import Figure



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
        

        self.temp_slices = np.array([[[0.0 for z in range(reactor.default_depth)] for x in range(len(reactor.default_layout))] for y in range(len(reactor.default_layout[0]))])
        self.neutron_slices = np.array([[[0.0 for z in range(reactor.default_depth)] for x in range(len(reactor.default_layout))] for y in range(len(reactor.default_layout[0]))])
        self.depth_range = range(len(self.temp_slices))


        self.temp_normalized = mpl.colors.Normalize(0.0, reactor.max_temp + 1.0)
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
        
        
        #Copied from my old maecalories code
        self.canvas = FigureCanvas(self.temp_fig)  # a gtk.DrawingArea
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.quit)
        self.window.set_default_size(600,900)
        self.window.set_title('Temparatures')
        # Have a box just in case
        self.main_box = gtk.HBox()
        self.window.add(self.main_box)
        self.main_box.pack_start(self.canvas, True, True)
        self.redraw_in_progress = False

        self.slice_cms = []
        # Set the data to axes
        for i in range(len(self.temp_slices)):
            row = i % self.fig_rows
            col = (i/self.fig_rows) % self.fig_cols
            # I hope these go as pointers cleanly (they don't see the redraw method)
            tmp = self.temps[row][col].pcolor(self.X,self.Y,self.temp_slices[i], norm=self.temp_normalized)
            self.slice_cms.append(tmp)
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
                    
        self.reports_expected /= len(self.temp_slices)
        # And recalculate the normalization again
        self.redraw()

        self.temp_reports_received = 0
        self.temp_full_reports_received = 0
        self.bus.add_signal_receiver(self.temp_report, dbus_interface = "fi.hacklab.reactorsimulator", signal_name = "emit_temp")
        self.neutron_reports_received = 0
        self.neutron_full_reports_received = 0
        #self.bus.add_signal_receiver(self.neutron_report, dbus_interface = "fi.hacklab.reactorsimulator", signal_name = "emit_neutrons")

        # This blocks, need to figure some other way to draw the canvas
        #plt.show()
        self.window.show_all()


    def quit(self, *args):
        self.loop.quit()

    def recalculate_normalizers(self):
        self.max_temp = self.temp_slices.item(self.temp_slices.argmax())
        #self.temp_normalized = mpl.colors.Normalize(0.0, self.max_temp + 1.0)
    

    def redraw(self):
        print "Redraw called on %f" % time.time()
        if self.redraw_in_progress:
            print "   But already in progress"
            return
        self.redraw_in_progress = True
        self.recalculate_normalizers()

        # Set the data to axes
        for i in range(len(self.temp_slices)):
            # Could we define the slices arrays as NP arrays already and save a bit of CPU time ?? 
            self.slice_cms[i].set_array(self.temp_slices[i].ravel())
            self.slice_cms[i].set_norm(self.temp_normalized)
        # I guess this could be optimized somehow by changing the values instead of recreating the whole thing
        #self.temp_cb = mpl.colorbar.ColorbarBase(self.temps[self.fig_rows-1][self.fig_cols-1], norm=self.temp_normalized, orientation='horizontal')
        #self.temp_cb.update_normal(self.temp_normalized)

        self.temp_fig.canvas.draw()
        self.redraw_in_progress = False
        print "Redraw complete on %f" % time.time()

    def temp_report(self, x, y, temp, sender):
        #print "temp_report called on %f" % time.time()
        self.temp_reports_received += 1
        if  (self.temp_reports_received % self.reports_expected == 0):
            self.temp_full_reports_received += 1
        if (self.temp_full_reports_received % 5 <> 0):
            # Process only every tenth *full* report so we have a hope of keeping up
            return
        #print "%d mod %d = %d" % (self.temp_reports_received, self.reports_expected, self.temp_reports_received % self.reports_expected)
        #print "temp_report started on %f" % time.time()
        for i in self.depth_range:
            self.temp_slices[i][x][y] = temp[i]
        #print "temp_report done on %f" % time.time()
        if  (self.temp_reports_received % self.reports_expected == 0):
            self.redraw()

    def neutron_report(self, x, y, neutrons, sender):
        self.neutron_reports_received += 1
        if  (self.neutron_reports_received % self.reports_expected == 0):
            self.neutron_full_reports_received += 1
        if (self.neutron_full_reports_received % 5 <> 0):
            # Process only every tenth *full* report so we have a hope of keeping up
            return
        for i in self.depth_range:
            self.neutron_slices[i][x][y] = neutrons[i]
        if  (self.neutron_reports_received % self.reports_expected == 0):
            self.redraw()

if __name__ == '__main__':
#    print "Use visualizer_launcher.py"
#    sys.exit(1)
    import dbus.mainloop.glib, gobject
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    
    # TODO: Add some nicer way to exit than ctrl-c
    bus = dbus.SessionBus()
    loop = gobject.MainLoop()
    state_instance = reactor_listener(bus, loop)
    loop.run()
        

