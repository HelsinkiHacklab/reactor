package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives.{Simulator, OutFlow, InFlow, Container}

/**
 * 
 */

class Turbine extends Container {

  val steamIn = fluidPort(InFlow)
  val steamOut = fluidPort(OutFlow)

  // TODO Electricity out, simulation - or simulate mechanical link to generators too (later)

  override protected def init(simulator: Simulator) {

  }


}