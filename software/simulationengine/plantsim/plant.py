class plant():
    """
      A plant, consisting of a set of components.
      Simulates component state with each tick, and sends update events for component changes.
    """

    def __init__(self):
        self.components = []



    def tick(self, duration_seconds):
        # Tick the components
        for component in self.components:
            component.tick(duration_seconds)