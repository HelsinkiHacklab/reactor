package fi.hacklab.reactor.primitives

/**
 * Connects two ports together.
 */
// TODO: Should this take care of moving matter on update? Maybe..  Or have container do that, then pipe doesn't have to be directly added to plant.

// TODO: Subclasses / functionality / effects / basic building blocks:
// * Pump - pressure in some direction, based on power input to pump and signal input
// * Filter
// * Valve
// * Heat exchange - don't move matter, just efficiently exchange heat?
case class Connection(a: Port, b: Port) {

  var flow_m3_per_s = 0.0

  def disconnect() {
    if (a != null) a.disconnect(this)
    if (b != null) b.disconnect(this)
    flow = 0.0
  }

  def connectsToPort(port: Port): Boolean = a == port || b == port


}