"""
Framebuffer info
"""

import subprocess, re

# mayber replace with ioctl eventually

def resolution():
    """
    Determine current framebuffer size

    returns (xsize, ysize)
    or
    raises exception if framebuffer size was not determined
    """
    output = subprocess.check_output(('/bin/fbset',))
    r = re.compile(r'geometry (?P<xres>\d+) (?P<yres>\d+) (?P<vxres>\d+) (?P<vyres>\d+)')
    m = r.search(output)
    if not m:
        raise RuntimeError("framebuffer size could not be determined")
    return int(m.group("xres")), int(m.group("yres"))

if __name__ == '__main__':
    print geometry()
