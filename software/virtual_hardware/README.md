# Virtual reactor hardware

PySide/QML versions of the physical control consoles, for testing the simulation engine

## Dependencies

    apt-get install python-pyside python-dbus python-yaml

Note that you need pyside version 1.0 or later, this means a fairly recent Ubuntu (11.10 for example)

## Running

Each physical part of the reactor is a separate program, to start all (two of the implemented ones) of them run

    python lid/lid.py &
    python rodcontrol/rodcontrol.py &

To make these do anything else than output signals on the D-BUS see the [middleware][1]

1: https://github.com/HelsinkiHacklab/reactor/tree/master/software/middleware

## TODO

  * Refactor the controllers to one baseclass
  * Figure out one good way to map the arDuBUS functionality to QML (now it's done in a bit of a mixed way)
  * Figure out how to maintain the pin numbers etc in sync when arDuBUS will use YAML mapping files and code
    generated from them.
