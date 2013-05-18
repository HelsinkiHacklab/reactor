#!/bin/bash -x

# Python and python libs
sudo apt-get install python python-pip python-pygame python-yaml python-zmq python-tornado libavahi-compat-libdnssd1 python-gobject python-pyside python-gst0.10
sudo pip install pybonjour
# Realpath required for calling the launchers via desktop links
sudo apt-get install realpath


