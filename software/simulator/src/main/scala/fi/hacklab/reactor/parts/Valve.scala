package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives.{Container, Simulator, Part}

/**
 * 
 */

class Valve extends Container {

  val a = fluidPort()
  val b = fluidPort()

  var openPercent = 0.0

  // TODO: Restrict flow

  override protected def init(simulator: Simulator) {
    
  }
}