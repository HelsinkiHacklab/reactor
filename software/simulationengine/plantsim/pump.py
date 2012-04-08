from component import component
from fluid import fluid
from port import port
import physics

class pump(component):

    def __init__(self, max_pressure_Pa = physics.medium_pump_pressure_Pa, height_m = 1, base_height_m = 0, area_m2 = physics.medium_pipe_size_m2, pump_length_m = 2):
        component.__init__(self)
        self.length_m = pump_length_m
        self.area_m2 = area_m2
        self.volume_m3 = self.area_m2 * self.length_m
        self.fluid = fluid(self.volume_m3, height_m, base_height_m)

        self.in_port  = self.fluid.add_port(port("in",  self.fluid, area_m2, pump_length_m/2.0, height_m))
        self.out_port = self.fluid.add_port(port("out", self.fluid, area_m2, pump_length_m/2.0, height_m))

        self.max_pressure_Pa = max_pressure_Pa
        self.activation = 0.5

    def adjust_power(self, activation):
        self.activation = activation
        if self.activation > 1.0: self.activation = 1.0
        if self.activation < 0.0: self.activation = 0.0

