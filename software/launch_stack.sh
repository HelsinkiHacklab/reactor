#!/bin/bash -ex
python simulationengine/simulation_launcher.py &
python simulationengine/visualizer_launcher.py &
for vh in $( find virtual_hardware/ -name '*.py' | grep -v \._* )
do
    python $vh &
done
python noisemaker/noisemaker_launcher.py &
python middleware/middleware_launcher.py &
