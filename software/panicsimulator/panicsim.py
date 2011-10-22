
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
        phantom_channels = [][]
        
        for i in range(0, 32):
            self.fuel_channels.append(fuel_channel(200, 100, 50, 100, 100, 100, 100))
        for x in range(0, 9):                

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
            
            
            
        for c in self.fuel_channels:
            c.flux += # Sum of adjacent channel outfluxes multiplied by fluxSpreadFactor * time
            c.temp += # Sum of adjacent channel outtemps multiplied by tempSpreadFactor * time
                
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









