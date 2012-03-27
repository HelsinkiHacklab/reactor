import dbus,time
 
bus = dbus.SessionBus()
mw = bus.get_object('fi.hacklab.reactorsimulator.middleware', '/fi/hacklab/reactorsimulator/middleware/bridge')


mw.led_gauge(0, 4, 350, 800)

