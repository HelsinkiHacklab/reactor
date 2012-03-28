from __future__ import with_statement
import dbus,time
import yaml

# Attach to the bus
bus = dbus.SessionBus()
l = bus.get_object('fi.hacklab.launchertest.launcher', '/fi/hacklab/launchertest/launcher')

# read,modify,write the config
with open('test.yml') as f:
    config = yaml.load(f)
config['cli_mod'] = time.time()
with open('test.yml', 'w') as f:
    yaml.dump(config, f)

# And call reload
l.reload()

# And remove the modification from the file
del(config['cli_mod'])
with open('test.yml', 'w') as f:
    config = yaml.dump(config, f)

print "call l.quit() when done"

