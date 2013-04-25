from __future__ import with_statement
import sys,os
import yaml



class codegen:
    def __init__(self, device_name, device_config):
        self.name = device_name
        self.config = device_config
        pass

    def parse_pin_numbers(self, numbers_and_aliases):
        ret = []
        for info in numbers_and_aliases:
            # Check if it's a dict defining pin and alias or just list of pins
            if type(info) == dict:
                ret.append(info['pin'])
            else:
                ret.append(info)
        return ret

    def prepare_sketch_file(self):
        self.sketch_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'generated', self.name)
        if not os.path.exists(self.sketch_dir):
            os.makedirs(self.sketch_dir)
        self.sketch_path = os.path.join(self.sketch_dir, self.name + '.ino')
        # Touch the file
        open(self.sketch_path, 'a').close()

    def add_bounce_include(self, code):
        if self.bounce_included:
            return code
        code += """#include <Bounce.h> // For some weird reason including this in the relevant .h file does not work\n"""
        self.bounce_included = True
        return code

    def add_i2c_include(self, code):
        if self.i2c_included:
            return code
        code += """#include <I2C.h> // For some weird reason including this in the relevant .h file does not work\n"""
        self.i2c_included = True
        return code

    def add_i2c_device_include(self, code):
        if self.i2c_device_included:
            return code
        code += """#include <i2c_device.h> // For some weird reason including this in the relevant .h file does not work\n"""
        self.i2c_device_included = True
        return code

    def generate_code(self):
        ret = ""
        
        # Some state tracking
        self.setup_i2c_init =  False
        self.bounce_included = False
        self.i2c_included = False
        self.i2c_device_included = False
        self.setup_pca9635_opencollector = False
        self.setup_wake_pca9635 = False
        
        # Defines
        if self.config.has_key('digital_in_pins'):
            ret = self.add_bounce_include(ret)
            ret += """#define ARDUBUS_DIGITAL_INPUTS { %s }\n""" % ", ".join(map(str, self.parse_pin_numbers(self.config['digital_in_pins'])))
        if self.config.has_key('digital_out_pins'):
            ret += """#define ARDUBUS_DIGITAL_OUTPUTS { %s }\n""" % ", ".join(map(str, self.parse_pin_numbers(self.config['digital_out_pins'])))
        if self.config.has_key('digital_pwmout_pins'):
            ret += """#define ARDUBUS_PWM_OUTPUTS { %s }\n""" % ", ".join(map(str, self.parse_pin_numbers(self.config['digital_pwmout_pins'])))
        if self.config.has_key('pca9535_boards'):
            self.setup_i2c_init = True
            ret = self.add_i2c_include(ret)
            ret = self.add_i2c_device_include(ret)
            ret += """#define ARDUBUS_PCA9535_BOARDS { %s }\n""" % ", ".join(map(str, self.config['pca9535_boards']))
   
            # Only check for I/O if boards are defined...
            if self.config.has_key('pca9535_inputs'):
                ret = self.add_bounce_include(ret)
                ret += """#define PCA9535_ENABLE_BOUNCE\n""" # This we might want to leave out to conserve memory...
                ret += """#define PCA9535_BOUNCE_OPTIMIZEDREADS\n"""
                ret += """#define ARDUBUS_PCA9535_INPUTS { %s }\n""" % ", ".join(map(str, self.parse_pin_numbers(self.config['pca9535_inputs'])))

            if self.config.has_key('pca9535_outputs'):
                ret += """#define ARDUBUS_PCA9535_OUTPUTS { %s }\n""" % ", ".join(map(str, self.parse_pin_numbers(self.config['pca9535_outputs'])))

            # This need to be included *after* the possible define of PCA9535_ENABLE_BOUNCE
            ret += """#include <pca9535.h> // For some weird reason including this in the relevant .h file does not work\n"""
        
        if self.config.has_key('pca9635RGBJBOL_boards'):
            self.setup_wake_pca9635 = True
            self.setup_pca9635_opencollector = True
            self.setup_i2c_init = True
            ret = self.add_i2c_include(ret)
            ret = self.add_i2c_device_include(ret)
            ret += """#include <pca9635.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635RGB.h> // For some weird reason including this in the relevant .h file does not work
#include <pca9635RGBJBOL.h> // For some weird reason including this in the relevant .h file does not work\n"""
            ret += """#define ARDUBUS_PCA9635RGBJBOL_BOARDS { %s }\n""" % ", ".join(map(str, self.config['pca9635RGBJBOL_boards']))

        if self.config.has_key('aircore_boards'):
            self.setup_i2c_init = True
            ret = self.add_i2c_include(ret)
            ret = self.add_i2c_device_include(ret)
            ret += """#define ARDUBUS_AIRCORE_BOARDS { %s }\n""" % ", ".join(map(str, self.config['aircore_boards']))

        if self.config.has_key('i2cascii_boards'):
            self.setup_i2c_init = True
            ret = self.add_i2c_include(ret)
            ret += """#define ARDUBUS_I2CASCII_BOARDS { %s }\n""" % ", ".join([ str(x['address']) for x in self.config['i2cascii_boards'] ])
            ret += """#define ARDUBUS_I2CASCII_BUFFER_SIZE %d\n""" % (max([ int(x['chars']) for x in self.config['i2cascii_boards'] ])+1)


        ret += """\n#include <ardubus.h>
void setup()
{
    Serial.begin(%s);
    Serial.println(F(""));
    Serial.println(F("Board: %s initializing"));\n""" % (self.config['_speed'], self.name)

        if self.setup_i2c_init:
            ret += """    
    I2c.timeOut(500); // 500ms timeout to avoid lockups
    I2c.pullup(false); //Disable internal pull-ups
    I2c.setSpeed(false); // Fast-mode support\n"""

        # Call ardubus setup
        ret += """    ardubus_setup();\n"""
        
        # post-setup operations
        if self.setup_pca9635_opencollector:
            ret += """    PCA9635.set_driver_mode(0x0);\n"""
        if self.setup_wake_pca9635:
            ret += """    PCA9635.set_sleep(0x0);\n"""
            
 
        # Setup done, output board name and define the loop
        ret += """    Serial.println(F("Board: %s ready"));
}

void loop()
{
    ardubus_update();
}\n""" % self.name
 
        return ret        

    def generate_sketch(self):
        self.prepare_sketch_file()
        with open(self.sketch_path, 'w') as f:
            f.write(self.generate_code())
        return True

if __name__ == '__main__':
    device_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'devices.yml')
    with open(device_config_file) as f:
        devices_config = yaml.load(f)
    general_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ardubus.yml')
    with open(general_config_file) as f:
        general_config = yaml.load(f)
    
    for device_name in devices_config.keys():
        device_config = devices_config[device_name]
        device_config['_speed'] = general_config['speed']

        #print repr(device_config)

        dev = codegen(device_name, device_config)
        

        if dev.generate_sketch():
            print "Wrote sketch %s" % dev.sketch_path

