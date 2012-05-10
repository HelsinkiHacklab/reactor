import dbus,time
 
bus = dbus.SessionBus()
mw = bus.get_object('fi.hacklab.reactorsimulator.middleware', '/fi/hacklab/reactorsimulator/middleware/bridge')
well_coords = [(1,2),(2,5),(4,1),(5,4)]

def reset_wells():
    for coords in well_coords:
        mw.led_gauge("well_%d_%d_temp" % coords, 0, 800)
        mw.led_gauge("well_%d_%d_neutrons" % coords, 0, 800)

#reset_wells()

