import launcher,dbus


my_signature = 'fi.hacklab.launchertest'

class my_launcher(launcher.baseclass):
    def __init__(self, mainloop, bus, **kwargs):
        launcher.baseclass(self, mainloop, bus, **kwargs)

    @dbus.service.method(my_signature + '.launcher')
    def quit(self):
        launcher.baseclass.quit(self)


launcher.main(my_launcher, my_signature)
