# Reactor simulator middleware

This act as an intermediate between the hardware (real or simulated) and the simulation engine.

# Dependencies

Make sure you can run the [virtual hardware][1], the [simulation engine][2] and [noisemaker][3]

# Running

Make sure you have the [simulation engine][2] and [noisemaker][3] running, start all of the runnable pieces of [virtual hardware][1] and then launch the middleware

    python middleware_launcher.py

When we get D-BUS activation working with these pieces things will get significantly simpler as D-BUS will simply start everything
as soon as we try to connect to the bus names they provide.

[1]: https://github.com/HelsinkiHacklab/reactor/tree/master/software/virtual_hardware
[2]: https://github.com/HelsinkiHacklab/reactor/tree/master/software/simulationengine
[3]: https://github.com/HelsinkiHacklab/reactor/tree/master/software/noisemaker

