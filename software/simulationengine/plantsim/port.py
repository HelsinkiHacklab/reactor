
import physics
import sys

class PortConnectionError(Exception): pass

class port():
    """
     A port of some component that can be connected to another one.
     Provides most recent calculated flow velocity (positive out, negative in),
     as well as pressure and material composition on the host component side.
    """

    def __init__(self, name, fluid_body, area_m2, length_m, relative_height_m = 0, pressure_Pa = physics.atmospheric_pressure_Pa):
        self.name = name
        self.fluid_body = fluid_body
        self.area_m2  = area_m2
        self.length_m = length_m
        self.relative_height_m = relative_height_m
        self.pressure_Pa = pressure_Pa
        self.connected_port = None

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


