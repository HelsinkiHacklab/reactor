#!/bin/bash -ex
# The visualizer does not have any use for a terminal
python simulationengine/visualizer_launcher.py &
# For others it's usefull for debugging
gnome-terminal --title="arDuBUS" -e "python arDuBUS/ardubus_launcher.py" &
gnome-terminal --title="Noisemaker" -e "python noisemaker/noisemaker_launcher.py" &
gnome-terminal --title="Simulationengine" -e "python simulationengine/simulation_launcher.py" &
sleep 5 # Give the others time to actually register on the bus before firing up the middleware that will throw a hissy fit if it doesn't seem them
gnome-terminal --title="Middleware" -e "python middleware/middleware_launcher.py" &
