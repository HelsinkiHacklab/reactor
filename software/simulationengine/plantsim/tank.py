
import component
import fluid
import port

class tank(component.component):

    def __init__(self, volume_m3):
        self.volume_m3 = volume_m3
        self.fluid = fluid.fluid(1, 20, 0.5) # Delivered with some initial fluid so as to not divide universe with zero


    def add_port(self, name, area_m2 = 0.25, length_m = 0.5, relative_height_m = 0):
        self._add_ports(port.port(name, self.fluid, area_m2, length_m, relative_height_m))



