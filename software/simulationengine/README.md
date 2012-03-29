# The actual simulation engine

This will run the simulation, idea is to be able to both save the simulation state to disk and to read it over dbus for further analysis

# Design

Basic idea is that just about everything is an object and all interactions between objects is via method call and/or signals,  each control-rod/fuell-well has N fuel cells that for each time unit trigger decay at some probability based on the control rod position and whenever a cell triggers decay it will also at some probability trigger decay for each neighbouring cell as well.

# Usage

Make sure you have the following packages (ubuntu/debian naming)

    python-dbus
    python-gobject
    python-yaml

Start with  python simulation_launcher.py

# Visualizer

Note, this is a bit slow since matplotlib is optimized for accuracy, not speed

Make sure you have the following packages in addition to above (ubuntu/debian naming)

    python-matplotlib

Start with  python visualizer_launcher.py

Then start the reactor and watch it veer out of control.
