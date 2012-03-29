# The actual simulation engine

This will run the simulation, idea is to be able to both save the simulation state to disk and to read it over dbus for further analysis

# Design

Basic idea is that just about everything is an object and all interactions between objects is via method call and/or signals,  each control-rod/fuell-well has N fuel cells that for each time unit trigger decay at some probability based on the control rod position and whenever a cell triggers decay it will also at some probability trigger decay for each neighbouring cell as well.

# Install dependencies

> sudo apt-get install python-yaml

# Usage

Start components:  

> python simulation_launcher.py &

> python visualization_launcher.py &
