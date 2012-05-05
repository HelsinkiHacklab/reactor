from __future__ import with_statement
import sys,os
import yaml

device_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'devices.yml')
general_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ardubus.yml')



#
#    def load_config(self):
#        """Loads (or reloads) the configuration file"""
#        if not self.config_file_path:
#            return False
#        with open(self.config_file_path) as f:
#            self.config = yaml.load(f)
#        return True
