
import physics

class fluid:
    """
     Represents the conditions of a body of fluid.
     For now, it is assumed the fluid is always water, either in liquid or gaseous (steam) form.
    """

    def __init__(self, mass_kg, temperature_C, steam_portion):
        self.mass_kg       = mass_kg       # Mass in this body of fluid.
        self.temperature_C = temperature_C # Temperature of the fluid.
        self.steam_portion = steam_portion # Portion of the fluid that is in gaseous form (bubbles etc), from 0 (0%) to 1 (100%).




    def pressure_Pa(self, volume_m3):
        """ Calculates the pressure in this body of fluid, in Pascals, given the volume it is contained in. """
        # TODO
        return physics.atmospheric_pressure_Pa

