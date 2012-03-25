package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives._

/**
 * 
 */

class SteamCondenser extends Container {


  val hotWaterIn = fluidPort(InFlow)
  val coolWaterIn = fluidPort(InFlow)
  val steamOut = fluidPort(OutFlow)
  val waterOut = fluidPort(OutFlow)


}