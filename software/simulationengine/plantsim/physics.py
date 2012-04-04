
# Various physics constants
bar_Pa                  = 100000 # 1 bar in Pascals
atmospheric_pressure_Pa = 101325 # Standard atmospheric pressure in Pascals

approximate_water_density = 1000 # kg / m3

# Some basic pipe sizes
large_pipe_size_m2 = 1.0
medium_pipe_size_m2 = 0.5

# Some basic pump pressures
small_pump_pressure_Pa  =  5000
medium_pump_pressure_Pa = 10000
large_pump_pressure_Pa  = 50000

small_heat_exchanger_area_m2 = 10
medium_heat_exchanger_area_m2 = 50
large_heat_exchanger_area_m2 = 100

# Gravitational force
earth_g = 9.81

# Material properties
def water_density(temperature_C):
    # TODO: Water density at 100 degrees is about 950, and at 300 degrees about 500, so we may need an approximate function
    return approximate_water_density

def water_viscosity(temperature_C, pressure_pa):
    # TODO: Find approximation
    return 1000.0


def water_pressure(temperature_C, depth_m, surface_pressure_Pa = atmospheric_pressure_Pa):
    return  surface_pressure_Pa + water_density(temperature_C) * depth_m * earth_g


