
# Various physics constants
bar_Pa                  = 100000 # 1 bar in Pascals
atmospheric_pressure_Pa = 101325 # Standard atmospheric pressure in Pascals

approximate_water_density = 1000 # kg / m3

# Some basic pipe sizes
large_pipe_size_m2 = 1.0
medium_pipe_size_m2 = 0.5

# Gravitational force
earth_g = 9.81

# Material properties
def water_density(temperature_C):
    # TODO: Water density at 100 degrees is about 950, and at 300 degrees about 500, so we may need an approximate function
    return approximate_water_density

def water_pressure(temperature_C, depth_m, surface_pressure_Pa = atmospheric_pressure_Pa):
    return  surface_pressure_Pa + water_density(temperature_C) * depth_m * earth_g