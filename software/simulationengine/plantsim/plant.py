class plant:
    """
      A plant, consisting of a set of components.
      Simulates component state with each tick, and sends update events for component changes.
    """

    def __init__(self):
        self.components = []

    def add(self, component):
        self.components.append(component)
        return component

    def update(self, duration_seconds):
        # Update the components
        for component in self.components:
            component.update(duration_seconds)