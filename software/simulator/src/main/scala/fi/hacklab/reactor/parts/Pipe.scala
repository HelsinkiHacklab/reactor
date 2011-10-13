package fi.hacklab.reactor.parts

/**
 * Connects two ports together.
 */
// TODO: Should this take care of moving matter on update? Maybe..  Or have container do that, then pipe doesn't have to be directly added to plant.
case class Pipe(a: Port, b: Port) {

  var flow = 0.0

  def disconnect() {
    if (a != null) a.disconnect(this)
    if (b != null) b.disconnect(this)
    flow = 0.0
  }

  def connectsToPort(port: Port): Boolean = a == port || b == port

}