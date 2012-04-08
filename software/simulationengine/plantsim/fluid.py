
import physics
from mathutil import clamp, lerp

class fluid:
    """
     Represents the conditions of a body of fluid.
     For now, it is assumed the fluid is always water, either in liquid or gaseous (steam) form.
    """

    def __init__(self, area_m2, height_m, base_height_m = 0, fill_amount = 0.7, open_roof = False, fixed_liquid_level=False, initial_temperature_C=physics.ambient_temperature_C):
        self.ports = {}

        self.base_height_m = base_height_m
        self.area_m2       = area_m2
        self.height_m      = height_m
        self.volume_m3     = area_m2 * height_m

        self.temperature_C = initial_temperature_C

        self.water_kg      = fill_amount * self.volume_m3 / physics.water_density(self.temperature_C)
        self.steam_kg      = 0.0

        self.liquid_level_m = fill_amount * self.height_m
        self.gas_pressure_Pa = physics.atmospheric_pressure_Pa
        self.surface_pressure_Pa = self.gas_pressure_Pa
        self.incoming_surface_pressure_Pa = 0.0
        self.open_roof = open_roof
        self.fixed_liquid_level = fixed_liquid_level


    def add_port(self, port):
        self.ports[port.name] = port
        return port

    def port(self, name):
        return self.ports[name]



    def gas_volume(self):
        return max(0.0, (self.height_m - self.liquid_level_m) * self.area_m2)



    def calculate_gas_pressure_Pa(self):
        if self.open_roof:
            return physics.atmospheric_pressure_Pa
        else:
            gas_volume = self.gas_volume()
            if gas_volume > 0:
                temp_K     = physics.celcius_to_kelvin(self.temperature_C)
                gas_moles  = self.steam_kg / (1000.0 * physics.molar_mass_water_g_per_mol)
                R          = physics.ideal_gas_constant
                return gas_moles * R * temp_K / gas_volume
            else:
                return 0.0


    def update(self, duration_s):
        """ Update fluid body """
        self.gas_pressure_Pa = self.calculate_gas_pressure_Pa()

        self.incoming_surface_pressure_Pa = 0.0
        if not self.open_roof:
            # Average incoming pressures, adjusted to the liquid surface
            num_ports = 0
            for name, port in self.ports.iteritems():
                depth = self.depth_at(port.height_m)
                incoming_pressure = port.get_other_pressure_Pa()
                adjusted_incoming_surface_pressure = incoming_pressure - depth * self.liquid_density() * physics.earth_g
                self.incoming_surface_pressure_Pa += adjusted_incoming_surface_pressure
                num_ports += 1
            if num_ports > 0:
                self.incoming_surface_pressure_Pa /= num_ports


        # Calculate surface pressure
        self.surface_pressure_Pa = self.incoming_surface_pressure_Pa
        if self.gas_volume() > 0:
            # There is some gas above the water surface, providing pressure down on it
            self.surface_pressure_Pa += self.gas_pressure_Pa



        # Calculate temperature change based on pressure change
        # TODO

        # Evaporate or condense water to change water to steam or the other way
        # TODO


    def calculate_flow(self, duration_s):
        for name, port in self.ports.iteritems():
            port.calculate_flow(duration_s)


    def execute_flow(self, duration_s):
        for name, port in self.ports.iteritems():
            port.execute_flow(duration_s)


    def absolute_liquid_level(self):
        return self.base_height_m + self.liquid_level_m

    def liquid_density(self):
        return physics.water_density(self.temperature_C)

    def gas_density(self):
        if self.open_roof:
            return physics.air_density
        else:
            gas_volume_m3 = self.gas_volume()
            if gas_volume_m3 > 0:
                return self.steam_kg / gas_volume_m3
            else:
                return 0.0

    def mass_kg(self):
        return self.water_kg + self.steam_kg

    def top(self):
        return self.base_height_m + self.height_m

    def depth_at(self, height_m):
        return max(0.0, self.absolute_liquid_level() - height_m)

    def pressure_at(self, height_m):
        return self.incoming_surface_pressure_Pa + \
               self.gas_pressure_Pa + \
               physics.earth_g * self.liquid_density() * self.depth_at(height_m)


    def remove_fluid(self, volume_m3, height_m):
        depth = self.depth_at(height_m)

        # TODO: Remove both liquid and gas if opening is on both sides of liquid surface

        liquid_portion = 0.0
        gas_portion = 0.0
        if depth > 0:
            liquid_portion = 1.0
        else:
            gas_portion = 1.0

        moved_water_kg = max(0.0, liquid_portion * volume_m3 * self.liquid_density())
        moved_steam_kg = max(0.0, gas_portion    * volume_m3 * self.gas_density())

        if not self.fixed_liquid_level:
            moved_water_kg = min(moved_water_kg, self.water_kg)
            self.water_kg -= moved_water_kg
        if not self.open_roof:
            moved_steam_kg = min(moved_steam_kg, self.steam_kg)
            self.steam_kg -= moved_steam_kg

        return moved_water_kg, moved_steam_kg, self.temperature_C

    def add_fluid(self, added_fluid):
        added_water_kg, added_steam_kg, temperature_C = added_fluid
        total_added_mass_kg = added_water_kg + added_steam_kg
        if total_added_mass_kg > 0:

            if not self.fixed_liquid_level:
                self.water_kg += added_water_kg
            if not self.open_roof:
                self.steam_kg += added_steam_kg

            if not self.open_roof and not self.fixed_liquid_level:
                # TODO: Different temperature capacity?
                portion = total_added_mass_kg / (total_added_mass_kg + self.mass_kg())
                self.temperature_C = lerp(self.temperature_C, temperature_C, portion)

