


class component:
    """ A component in a plant. """

    def __init__(self, name):
        self.fluids = []
        self.name = name


    def _add_fluid(self, fluid):
        self.fluids.append(fluid)
        return fluid




    def update_pressure(self, duration_s):
        for fluid in self.fluids:
            fluid.update(duration_s)


    def calculate_flow(self, duration_s):
        for fluid in self.fluids:
            fluid.calculate_flow(duration_s)


    def execute_flow(self, duration_s):
        for fluid in self.fluids:
            fluid.execute_flow(duration_s)


