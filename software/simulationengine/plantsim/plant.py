import time

class plant:
    """
      A plant, consisting of a set of components.
      Simulates component state with each tick, and sends update events for component changes.
    """

    def __init__(self):
        self.components   = []
        self.stopped      = False
        self.step_delay_s = 0.2

    def add(self, component):
        self.components.append(component)
        return component


    def update_pressure(self, duration_s):
        for component in self.components:
            component.update_pressure(duration_s)


    def calculate_flow(self, duration_s):
        for component in self.components:
            component.calculate_flow(duration_s)

    def execute_flow(self, duration_s):
        for component in self.components:
            component.execute_flow(duration_s)


    def update(self, duration_s):
        # Calculate pressures
        self.update_pressure(duration_s)

        # Adjust temperature based on pressure change
        # mass / volume, temperature

        # Calculate flow
        # pressure difference, take pumps, vents into account
        self.calculate_flow(duration_s)

        # Move mass and fluid properties according to flow
        self.execute_flow(duration_s)


    def start(self):
        while not self.stopped:
            # TODO: Calculate step delay
            self.update(self.step_delay_s)

            # Sleep
            time.sleep(self.step_delay_s)



    def stop(self):
        self.stopped = True


