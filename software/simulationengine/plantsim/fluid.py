
import physics
from mathutil import clamp, lerp

class fluid:
    """
     Represents the conditions of a body of fluid.
     For now, it is assumed the fluid is always water, either in liquid or gaseous (steam) form.
    """

    def __init__(self, volume_m3, size_y_m, base_height_m = 0, fill_amount = 0.9):
        self.volume_m3     = volume_m3     # The volume of the container
        self.temperature_C = physics.ambient_temperature_C
        self.water_kg      = fill_amount * volume_m3 / physics.water_density(self.temperature_C)
        self.steam_kg      = 0.0
        self.pressure_Pa   = physics.atmospheric_pressure_Pa
        self.size_y_m      = size_y_m
        self.base_height_m = base_height_m


    def update_pressure(self, duration_s):
        """ Calculates the pressure in this body of fluid, in Pascals, based on the volume it is contained in, and the current mass, temperature, and steam percent. """
        old_pressure     = self.pressure_Pa
        self.pressure_Pa = physics.atmospheric_pressure_Pa
        pressure_change_Pa = self.pressure_Pa - old_pressure

        # Calculate temperature based on pressure change
        self.temperature_C = self.temperature_C

    def water_density(self):
        return physics.water_density(self.temperature_C)

    def steam_density(self):
        steam_volume_m3 = self.volume_m3 * (1.0 - self.get_water_volume_portion())
        if steam_volume_m3 > 0:
            return self.steam_kg / steam_volume_m3
        else:
            return 0.0

    def get_water_volume_portion(self):
        wv = self.water_kg / self.water_density()
        return clamp(wv / self.volume_m3, 0.0, 1.0)

    def get_mass_kg(self):
        return self.water_kg + self.steam_kg

    def pressure_at(self, height_m):
        # TODO: Calculate pressure at specified height, based on amount
        # of volume above the height, and its density
        return self.get_mass_kg()
        #return physics.atmospheric_pressure_Pa


    def remove_fluid(self, volume_m3, relative_height_m):
        water_portion  = self.get_water_volume_portion()
        steam_portion  = 1.0 - water_portion
        water_density = self.water_density()
        steam_density = self.steam_density()

        moved_water_kg = clamp(water_portion * volume_m3 * water_density, 0.0, self.water_kg)
        moved_steam_kg = clamp(steam_portion * volume_m3 * steam_density, 0.0, self.steam_kg)
        self.water_kg -= moved_water_kg
        self.steam_kg -= moved_steam_kg
        return moved_water_kg, moved_steam_kg, self.temperature_C

    def add_fluid(self, added_fluid):
        added_water_kg, added_steam_kg, temperature_C = added_fluid
        total_added_mass_kg = added_water_kg + added_steam_kg
        if total_added_mass_kg > 0:
            self.water_kg += added_water_kg
            self.steam_kg += added_steam_kg

            # TODO: Different temperature capacity?
            portion =  total_added_mass_kg / (total_added_mass_kg + self.get_mass_kg())
            self.temperature_C = lerp(self.temperature_C, temperature_C, portion)

