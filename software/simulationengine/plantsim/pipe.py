from component import component
from fluid import fluid
from port import port
import physics
import math

class pipe(component):

    def __init__(self, length_m = 20.0, start_height_m = 0.0, end_height_m = 0.0, area_m2 = physics.medium_pipe_size_m2):
        component.__init__(self)
        self.length_m = length_m
        self.area_m2 = area_m2
        self.volume_m3 = area_m2 * length_m
        base_h = min(start_height_m, end_height_m)
        h      = max(start_height_m, end_height_m) - base_h
        self.fluid = fluid(self.volume_m3, h, base_h)

        self.in_port  = self._add_port(port("in_port", self.fluid, area_m2, length_m/2.0, start_height_m))
        self.out_port = self._add_port(port("out_port",   self.fluid, area_m2, length_m/2.0, end_height_m))




