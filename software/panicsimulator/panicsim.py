
print "In Soviet Russia, Code Breaks You"


# A trivial example for listening signals on the bus

import gobject
import dbus
import dbus.service
import dbus.mainloop.glib
import random
from time import sleep

from collections import namedtuple
import threading

class fuel_channel():
    def __init__(self, temp, flux, rodpos, pressure, fluxout, outtemp, 
                 cooling, rodup, roddown, rodstepped):
                 self.temp = temp
                 self.flux = flux
                 self.rodpos = rodpos
                 self.pressure = pressure
                 self.fluxout = fluxout
                 self.outtemp = outtemp
                 self.cooling = cooling
                 self.rodup = rodup
                 self.roddown = roddown
                 self.rodstepped = rodstepped

fluxSpreadFactor = 0.01
tempSpreadFactor = 0.01
rodEffectOnFlux = 0.01
fluxHeatGeneration = 0.01
coolingEffectOnTemp = 0.01
normalCooling = 1.0
rodMoveSpeed = 10
coolingStompIncrease = 10
fluxDissipation = 0.01
coolDownSpeed = 1
grid_w = 7
grid_h = 7
explodeTemp = 1000
recoverTemp = 500

rodEffectOnTemp = 10

tickTime = 0.01

highestTemp = 0
exploding = False
timeCounter = 0



class reactor(dbus.service.Object):


    def __init__(self, bus):
        self.object_name = 'reactor'
        self.object_path = '/fi/hacklab/ardubus/' + self.object_name
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
        
        for i in range(0, 33):
            self.fuel_channels.append(fuel_channel(200, 100, 50, 100, 100, 100, 100, False, False, False))
        
        self.simulator_thread = threading.Thread(target=self.simulator_loop)
        self.simulator_thread.setDaemon(1)
        self.simulator_thread.start()

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
        
    def simulator_loop(self):
        while True:
            self.simulate_step(tickTime)
            sleep(tickTime)  

                           
    def simulate_step(self, time):
        global exploding
        global highestTemp
        global timeCounter
        highestTemp = 0
        for c in self.fuel_channels:
            #print type(c), c, c.temp
            highestTemp = max(highestTemp, c.temp)
            #c.temp = 6
            #c.temp += c.flux * fluxHeatGeneration * time
            #c.temp -= c.cooling * coolingEffectOnTemp * time 
            #c.flux += (c.rodpos - 50) * rodEffectOnFlux * time
            #c.flux *= (1.0 - fluxDissipation)
                        
            if c.rodup:
                c.rodpos += rodMoveSpeed * time
                if c.rodpos > 100:
                    c.rodpos = 100
            if c.roddown:
                c.rodpos -= rodMoveSpeed * time
                if c.rodpos < 0:
                    c.rodpos = 0
            
            c.temp += (c.rodpos - 50) * rodEffectOnTemp * time
            c.temp += random.uniform(-0.1, 0.1)
            c.outtemp = c.temp
            
            if c.rodstepped:
                #c.cooling += coolingStompIncrease
                c.temp -= 100
                c.outtemp += 50
                c.rodstepped = False

            #if (c.cooling > normalCooling):
            #    c.cooling -= coolDownSpeed * time
            
            #c.outflux = c.flux
            
            
            
        #for c in self.fuel_channels:
        #    c.flux += # Sum of adjacent channel outfluxes multiplied by fluxSpreadFactor * time
        #    c.temp += # Sum of adjacent channel outtemps multiplied by tempSpreadFactor * time
        for i, currentRod in enumerate(self.ph_channels):
            if currentRod !=None:
                #print i, currentRod
                currentRod = self.fuel_channels[currentRod]
                neighbors = self.get_neighbours(i)
                if len(neighbors)  > 0:
                    #currentRod.flux = sum( [neigborRod.flux for neigborRod in neighbors] ) * fluxSpreadFactor * time 
                    currentRod.temp = currentRod.temp * (1.0 - tempSpreadFactor) + tempSpreadFactor * sum( [neigborRod.temp for neigborRod in neighbors] ) / len(neighbors)
                
                
        timeCounter += tickTime
        if (timeCounter > 1):
          roundCounter = 0
          for i, c in enumerate(self.fuel_channels):
              self.control_rod_pos(i, c.rodpos)

        # TODO: For the four measurement rods, send out flux and temperature readings.       
        
        if ((highestTemp > explodeTemp) and not exploding):
            # TODO: Play explode sound
            print "Exploded"
            exploding = True
        if ((highestTemp < recoverTemp) and exploding):
            exploding = False
            print "Explosion end"
        print "Maxtemp ", highestTemp   
        

if __name__ == '__main__':
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


    bus = dbus.SessionBus()
    recactor = reactor(bus)

    
    loop = gobject.MainLoop()
    loop.run()









