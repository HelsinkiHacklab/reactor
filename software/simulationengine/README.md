# The actual simulation engine

This will run the simulation, idea is to be able to both save the simulation state to disk and to read it over dbus for further analysis

# Design

Basic idea is that just about everything is an object and all interactions between objects is via method call and/or signals,  each control-rod/fuell-well has N fuel cells that for each time unit trigger decay at some probability based on the control rod position and whenever a cell triggers decay it will also at some probability trigger decay for each neighbouring cell as well.

# Install dependencies

## Simulation engine

    sudo apt-get install python-yaml python-dbus python-gobject

## Visualizer

    sudo apt-get install python-matplotlib

# Usage


## Starting the simulation

    python simulation_launcher.py &

## Starting the visualizer

    python visualizer_launcher.py &

Note, the visualizer is a bit slow since matplotlib is optimized for accuracy, speed is nice but accurate is better...

For this reason the visualizer rate limits itself only displaying every fifth complete signal set.

