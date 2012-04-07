
import physics
import sys

class PortConnectionError(Exception): pass

class port:
    """
     A port of some component that can be connected to another one.
     Provides most recent calculated flow velocity (positive out, negative in),
     as well as pressure and material composition on the host component side.
    """


    def __init__(self, name, fluid_body, area_m2, length_m, relative_height_m = 0):
        self.name = name
        self.fluid_body = fluid_body
        self.area_m2  = area_m2
        self.length_m = length_m
        self.relative_height_m = relative_height_m
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
        vessel_pressure = self.fluid_body.pressure_at(self.relative_height_m)
        # TODO: Calculate pressure drop over pipe based on flow
        return vessel_pressure


    def calculate_flow(self, duration_s):
        if self.connected_port is not None:
            # Get pressure on both sides of the connection
            own_pressure   = self.get_pressure_Pa()
            other_pressure = self.connected_port.get_pressure_Pa()
            pressure_difference = own_pressure - other_pressure
            # TODO: Calculate flow based on pressure difference
            self.flow_m3_per_s = pressure_difference
        else:
            self.flow_m3_per_s = 0.0


    def execute_flow(self, duration_s):
        if self.flow_m3_per_s > 0 and self.connected_port is not None:
            volume_m3 = self.flow_m3_per_s * duration_s
            self.connected_port.add_fluid(self.fluid_body.remove_fluid(volume_m3, self.relative_height_m))
            print("moving "+str(volume_m3)+"m3 from " + self.name + " to " + self.connected_port.name)


    def add_fluid(self, moved_fluid):
        self.fluid_body.add_fluid(moved_fluid)
