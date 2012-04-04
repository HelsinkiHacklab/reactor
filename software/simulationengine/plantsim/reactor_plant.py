
from component import component
from fluid import fluid
from port import port
from pipe import pipe
from river import river
from tank import tank
from plant import plant
from pump import pump
from valve import valve
from heat_exchanger import heat_exchanger
import physics

class reactor_plant(plant):

    def __init__(self):
        plant.__init__(self)
        self.setup_plant()


    def setup_plant(self):
        ## River water cooling circuit:

        # Water intake from river
        river_intake1 = self.add(river())
        river_intake2 = self.add(river())

        # River pumps
        river_pump1 = self.add(pump(physics.large_pump_pressure_Pa))
        river_pump2 = self.add(pump(physics.large_pump_pressure_Pa))
        river_pump1.in_port.connect(river_intake1.port)
        river_pump2.in_port.connect(river_intake2.port)

        # Backflow valves for pumps
        river_valve1 = self.add(valve())
        river_valve2 = self.add(valve())
        river_valve1.in_port.connect(river_pump1.out_port)
        river_valve2.in_port.connect(river_pump2.out_port)

        # Tank that combines inflows from river pumps
        river_in_tank = self.add(tank(10))
        river_in_tank.add_port("in1").connect(river_valve1.out_port)
        river_in_tank.add_port("in2").connect(river_valve2.out_port)
        river_tank_out_port = river_in_tank.add_port("out")
        river_in_pipe = self.add(pipe(30, area_m2=physics.large_pipe_size_m2))
        river_in_pipe.in_port.connect(river_tank_out_port)

        # Steam condenser
        steam_condenser = self.add(heat_exchanger())
        steam_condenser.a_in.connect(river_in_pipe.out_port)

        # River waste-water pipe
        river_out = self.add(river())
        river_out_pipe = self.add(pipe(40, area_m2=physics.large_pipe_size_m2))
        river_out_pipe.in_port.connect(steam_condenser.a_out)
        river_out_pipe.out_port.connect(river_out.port)


        ## Steam circuit:



        ## Primary cooling circuit:



        ## Electric power circuit:

