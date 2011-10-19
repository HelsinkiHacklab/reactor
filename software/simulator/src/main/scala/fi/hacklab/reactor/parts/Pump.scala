package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives._

/**
 * Create a pressure gradient from the input to the output.
 */
class Pump extends Container {

  val in  = fluidPort(InFlow, () => pressure - pumpPressure / 2)
  val out = fluidPort(OutFlow, () => pressure + pumpPressure / 2)

  val activityPercent = 1
  val maxPumpPressure = 1

  var pumpPressure = 0
  var powerUse_W = 0
  


  protected override def init(simulator: Simulator) {
    simulator.addUpdate('update) { time: Double =>

      pumpPressure = maxPumpPressure * activityPercent


    // TODO: Get required power from power lines

    // TODO: Acquired power affects displacement factor

    // TODO: Doesn't work well if there is much steam in chambers
    }
  }




}