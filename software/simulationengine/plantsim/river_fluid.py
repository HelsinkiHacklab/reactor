import physics

class river_fluid:
    def __init__(self, temperature_C, surface_height_m = 0.0):
        self.temperature_C = temperature_C

    def water_density(self):
        return physics.water_density(self.temperature_C)

    def remove_fluid(self, volume_m3, relative_height_m):
        moved_water_kg = volume_m3 * self.water_density()
        return moved_water_kg, 0.0, self.temperature_C

    def add_fluid(self, added_fluid):
        pass

    def pressure_at(self, height_m):
        # TODO: Calculate pressure at specified height, based on depth, density, and airpressure
        wp = -min(height_m, 0) * self.water_density() + physics.atmospheric_pressure_Pa
        return wp
