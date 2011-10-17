package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives._

/**
 * Create a pressure gradient from the input to the output.
 */
class Pump extends Container {

  val in  = makePort(InFlow)
  val out = makePort(OutFlow)

  val activityFactor = 1
  val maxPumpPressure = 1

  var pumpPressure = 0

  override def getPressure(port: Port): Double = {
    if (port == in) super.getPressure(port) - pumpPressure * 0.5
    else if (port == out) super.getPressure(port) + pumpPressure * 0.5
  }

  def update(time_s: Double) {
    pumpPressure = maxPumpPressure * activityFactor

    // TODO: Get required power from power lines

    // TODO: Acquired power affects displacement factor

    // TODO: Doesn't work well if there is much steam in chambers
  }

}