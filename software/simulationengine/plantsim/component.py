


class component:
    """ A component in a plant. """

    def __init__(self):
        self.ports = {}
        self.fluids = []


    def _add_port(self, port):
        self.ports[port.name] = port
        return port

    def _add_fluid(self, fluid):
        self.fluids.append(fluid)
        return fluid

    def port(self, name):
        return self.ports[name]


    def connect_port(self, name, other_port):
        """ Connect specified port to the other port.  Neither port should be connected anywhere before."""
        self.port(name).connect(other_port)



    def update_pressure(self, duration_s):
        for fluid in self.fluids:
            fluid.update_pressure(duration_s)


    def calculate_flow(self, duration_s):
        for name, port in self.ports.iteritems():
            port.calculate_flow(duration_s)


    def execute_flow(self, duration_s):
        for name, port in self.ports.iteritems():
            port.execute_flow(duration_s)


