


class component():
    """ A component in a plant. """

    def __init__(self):
        self.ports = {}


    def _add_port(self, port):
        self.ports[port.name] = port


    def port(self, name):
        return self.ports[name]


    def connect_port(self, name, other_port):
        """ Connect specified port to the other port.  Neither port should be connected anywhere before."""
        self.port(name).connect(other_port)


    def update(self, duration_s):
        # TODO 
        # 

