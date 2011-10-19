package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives.{Simulator, Container}

/**
 * 
 */

class Branch extends Container {


  val left    = fluidPort()
  val right   = fluidPort()
  val up      = fluidPort()
  val down    = fluidPort()
  val forward = fluidPort()
  val back    = fluidPort()


}