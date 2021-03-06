
from component import component
from fluid import fluid
from port import port
import physics

class river(component):
    """ A pipe connected to a river or sea, at some depth. """

    def __init__(self, name, height_m=-2.0, pipe_size_m2=physics.large_pipe_size_m2, pipe_length_m=20.0, river_temperature_C=18.0):
        component.__init__(self, name)
        self.height_m = height_m

        self.river_water = self._add_fluid(fluid(name, 100, 10, -5, 0.5, True, True, river_temperature_C))
        self.port = self.river_water.add_port(port("river", self.river_water, pipe_size_m2, pipe_length_m, height_m))


    def fluids(self):
        return [fluid]




