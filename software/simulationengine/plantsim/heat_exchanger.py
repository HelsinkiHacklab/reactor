from component import component
from fluid import fluid
from port import port
import physics

class heat_exchanger(component):

    # TODO: sensible parameters, find out typical values used in industry,
    # or maybe calculate manually based on shell and tube heat exchanger
    def __init__(self,
                 heat_transfer_coefficient = 1,
                 pressure_drop_Pa = 500,
                 a_volume_m3 = 10,
                 b_volume_m3 = 10,
                 contact_area_m2 = physics.medium_heat_exchanger_area_m2,
                 a_pipe_size_m2 = physics.medium_pipe_size_m2,
                 b_pipe_size_m2 = physics.medium_pipe_size_m2,
                 connector_lengths_m = 0.5,
                 height_m=5.0,
                 base_height_m=0):

        component.__init__(self)

        self.a_volume_m3 = a_volume_m3
        self.b_volume_m3 = b_volume_m3
        self.a_fluid = fluid(self.a_volume_m3, height_m, base_height_m) # Delivered with some initial fluid so as to not divide universe with zero
        self.b_fluid = fluid(self.b_volume_m3, height_m, base_height_m) # Delivered with some initial fluid so as to not divide universe with zero

        self.a_in  = self.a_fluid.add_port(port("a_in",  self.a_fluid, a_pipe_size_m2, connector_lengths_m, height_m))
        self.a_out = self.a_fluid.add_port(port("a_out", self.a_fluid, a_pipe_size_m2, connector_lengths_m, height_m))
        self.b_in   = self.b_fluid.add_port(port("b_in",   self.b_fluid,  b_pipe_size_m2,  connector_lengths_m, height_m))
        self.b_out  = self.b_fluid.add_port(port("b_out",  self.b_fluid,  b_pipe_size_m2,  connector_lengths_m, height_m))

        self.contact_area_m2 = contact_area_m2
        self.heat_transfer_coefficient = heat_transfer_coefficient
        self.pressure_drop_Pa = pressure_drop_Pa


