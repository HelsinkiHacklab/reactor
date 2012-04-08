
import physics
import sys

class PortConnectionError(Exception): pass

class port:
    """
     A port of some component that can be connected to another one.
     Provides most recent calculated flow velocity (positive out, negative in),
     as well as pressure and material composition on the host component side.
    """


    def __init__(self, name, fluid_body, area_m2, length_m, height_m = 0):
        self.name = name
        self.fluid_body = fluid_body
        self.area_m2  = area_m2
        self.length_m = length_m
        self.height_m = height_m
        self.connected_port = None
        self.flow_m3_per_s = 0.0

    def connect(self, other_port):
        """ Connect this port to the other port.  The ports should not already be connected. """
        # This port and the other port should not be connected before
        if other_port is None: raise PortConnectionError("Attempt to connect port '"+self.name+"' to None port.")
        if other_port is self: raise PortConnectionError("Attempt to connect port '"+self.name+"' to itself.")
        if self.connected_port is not None: raise PortConnectionError("Attempt to connect port '"+self.name+"' to a new port '"+other_port.name+"', but it is already connected to a port.")
        if other_port.connected_port is not None: raise PortConnectionError("Attempt to connect port '"+self.name+"' to a port '"+other_port.name+"' that is already connected.")

        # Connect ports
        self.connected_port = other_port
        other_port.connected_port = self


    def get_pressure_Pa(self):
        vessel_pressure = self.fluid_body.pressure_at(self.height_m)
        # TODO: Calculate pressure drop over pipe based on flow
        return vessel_pressure

    def get_other_pressure_Pa(self):
        if self.connected_port is not None:
            return self.connected_port.get_pressure_Pa()
        else:
            return 0.0


    def calculate_flow(self, duration_s):
        # TODO: Don't try to fill with more liquid + gas than what own (and other incoming?) pressure(s) would allow
        if self.connected_port is not None:
            # Get pressure on both sides of the connection
            own_pressure   = self.get_pressure_Pa()
            other_pressure = self.connected_port.get_pressure_Pa()
            pressure_difference = own_pressure - other_pressure
            # TODO: Calculate flow based on pressure difference
            self.flow_m3_per_s = pressure_difference / 100
        else:
            self.flow_m3_per_s = 0.0


    def execute_flow(self, duration_s):
        # TODO: Check that it is not overfilled (maintain incompressible liquid invariant)
        if self.flow_m3_per_s > 0 and self.connected_port is not None:
            volume_m3 = self.flow_m3_per_s * duration_s
            self.connected_port.add_fluid(self.fluid_body.remove_fluid(volume_m3, self.height_m))
            print("moving "+str(volume_m3)+"m3 from " + self.name + " to " + self.connected_port.name + " that now has " + str(self.connected_port.fluid_body.water_kg) + " kg water")


    def add_fluid(self, moved_fluid):
        self.fluid_body.add_fluid(moved_fluid)
