
print "In Soviet Russia, Code Breaks You"


# A trivial example for listening signals on the bus

import gobject
import dbus
import dbus.service
import dbus.mainloop.glib

from collections import namedtuple

fuel_channel = namedtuple('temp flux rodpos pressure fluxout outtemp cooling rodup roddown rodstepped')

fluxSpreadFactor = 0.01
tempSpreadFactor = 0.01
rodEffectOnFlux = 0.01
fluxHeatGeneration = 0.01
coolingEffectOnTemp = 0.01
normalCooling = 1.0
rodMoveSpeed = 0.5
coolingStompIncrease = 10
grid_w = 7
grid_h = 7

class ardubus(dbus.service.Object):
    def __init__(self, bus):
        self.object_name = 'reactor'
        self.object_path = '/fi/hacklab/ardubus/' + object_name
        self.bus_name = dbus.service.BusName('fi.hacklab.ardubus', bus=bus)
        dbus.service.Object.__init__(self, self.bus_name, self.object_path)
        self.bus = bus
        
        # We can either listen all signals on the interface regardles of the board or specify we want to listen only to specific board
        self.bus.add_signal_receiver(self.controlRodUp, dbus_interface = "fi.hacklab.ardubus", signal_name = "control_rod_up")
        self.bus.add_signal_receiver(self.controlRodDown, dbus_interface = "fi.hacklab.ardubus", signal_name = "control_rod_down")
         self.bus.add_signal_receiver(self.controlRodStepped, dbus_interface = "fi.hacklab.ardubus", signal_name = "control_rod_stepped")       
         
        self.fuel_channels = []
        self.ph_channels = [None, None,    0,   1,    2, None, None, 
                            None,    3, None,   4,    5,    6, None,
                               7,    8,    9,  10,   11, None,   12,
                              13,   14,   15,  16,   17,   18,   19,   
                              20,  None,  21,  22,   23,   24,   25,
                            None,    26,  27,  28, None,   29, None,
                            None,  None,  30,  31,   32, None, None]
        
        for i in range(0, 32):
            self.fuel_channels.append(fuel_channel(200, 100, 50, 100, 100, 100, 100))
    
    def get_neighbours(self, index):
        neighbours = []
        for x in range(-1, 1):
            for y in range(-1, 1):
                nindex = y * grid_w + x
                if nindex > 0 and nindex < grid_w * grid_h:
                    nitem = self.ph_channels[nindex]
                    if nitem:
                        neighbours.append(self.fuel_channels[nitem])
        return neighbours

    def signal_received(self, *args, **kwargs):
        print "Got args: %s" % repr(args)
        print "Got kwargs: %s" % repr(kwargs)

    def controlRodUp(self, pin, state):
        self.fuel_channels[pin].rodup = state

    def controlRodDown(self, pin, state):
        self.fuel_channels[pin].roddown = state
        
    def controlRodStepped(self, pin, state):
        if state:
            self.fuel_channels[pin].rodstepped = state
    
    @dbus.service.signal('fi.hacklab.ardubus')
    def control_rod_pos(self, index, value):
        pass 
               
    def simulate_step(self, time):
        for c in self.fuel_channels:
            c.temp += c.flux * fluxHeatGeneration * time
            c.temp -= c.cooling * coolingEffectOnTemp * time 
            c.flux += (c.rodpos - 50) * rodEffectOnFlux * time
            
            if c.rodup:
                c.rodPos += rodMoveSpeed * time
                if c.rodPos > 100:
                    c.rodPos = 100
            if c.roddown:
                c.rodPos -= rodMoveSpeed * time
                if c.rodPos < 0:
                    c.rodPos = 0
            
            if c.rodstepped:
                c.cooling += coolingStompIncrease
                c.rodstepped = False
            if (c.cooling > normalCooling):
                c.cooling -= cooldownSpeed * time
            
            c.outflux = c.flux
            c.outtemp = c.temp
            
            
            
        #for c in self.fuel_channels:
        #    c.flux += # Sum of adjacent channel outfluxes multiplied by fluxSpreadFactor * time
        #    c.temp += # Sum of adjacent channel outtemps multiplied by tempSpreadFactor * time
        for i, i2 in enumerate(self.ph_channels):
            if i2:
                item = self.get_neighbours(i)
                i2.flux = sum( [i.flux for i in item] ) / len(item)
                
        for i, c in enumerate(self.fuel_channels):
            self.control_rod_pos(i, c.rodpos)

        # TODO: For the four measurement rods, send out flux and temperature readings.       
        

if __name__ == '__main__':
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


    bus = dbus.SessionBus()
    recactor = reactor(bus)

    loop = gobject.MainLoop()
    loop.run()









