

from component import component
from fluid import fluid
from port import port
import physics

class tank(component):

    def __init__(self, volume_m3, height_m, base_height_m = 0, initial_fill_rate = 0.7):
        component.__init__(self)
        self.fluid = fluid(volume_m3/height_m, height_m, base_height_m, initial_fill_rate)

    def fluids(self):
        return [fluid]

    def add_port(self, name, area_m2 = 0.25, length_m = 0.5, relative_height_m = 0):
        return self.fluid.add_port(port(name, self.fluid, area_m2, length_m, relative_height_m))


