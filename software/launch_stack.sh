#!/bin/bash -ex
python simulationengine/simulation_launcher.py &
python simulationengine/visualizer_launcher.py &
for vh in $( find virtual_hardware/ -name '*.py' | grep -v '\._' )
do
    python $vh &
done
python noisemaker/noisemaker_launcher.py &
sleep 7 # Give the others time to actually register on the bus before firing up the middleware that will throw a hissy fit if it doesn't seem them
python middleware/middleware_launcher.py &
