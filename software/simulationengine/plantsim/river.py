
from component import component
from fluid import fluid
from port import port
import physics
from river_fluid import river_fluid

class river(component):
    """ A pipe connected to a river or sea, at some depth. """

    def __init__(self, height_m=-2.0, pipe_size_m2=physics.large_pipe_size_m2, pipe_length_m=20.0, river_temperature_C=18.0):
        component.__init__(self)
        self.height_m = height_m

        self.river_water = river_fluid(river_temperature_C)

        pressure_Pa = physics.water_pressure(river_temperature_C, height_m)
        self.port = self._add_port(port("river", self.river_water, pipe_size_m2, pipe_length_m, height_m))


    def fluids(self):
        return [fluid]




