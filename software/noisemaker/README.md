# DBUS Audio server

Currently possible to play named samples or predefined sequences/loops, uses Gstreamer & ALSAsink so this process
does not need to think about mixing.

Currently should do everything we *actually* need.

## Wishlist

  - Autogenerate loop_id and respond with that, so that the callee does not need to do that themselves (first checking the active loops list)
  - Specifying fades on software level instead of making them part of the samples ?
  - 3D audio (specifying sound location)
  - JACK & explicit multichannel support (use with multiple speakers with or without 3D audio for even better sound source control)


