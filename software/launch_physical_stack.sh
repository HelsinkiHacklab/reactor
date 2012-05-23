#!/bin/bash -ex
TPROG="gnome-terminal -e "
# The visualizer does not have any use for a terminal
python simulationengine/visualizer_launcher.py &
# For others it's usefull for debugging
$TPROG "python arDuBUS/ardubus_launcher.py" &
$TPROG "python noisemaker/noisemaker_launcher.py" &
$TPROG "python simulationengine/simulation_launcher.py" &
sleep 5 # Give the others time to actually register on the bus before firing up the middleware that will throw a hissy fit if it doesn't seem them
$TPROG "python middleware/middleware_launcher.py" &
