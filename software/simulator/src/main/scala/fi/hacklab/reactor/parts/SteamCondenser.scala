package fi.hacklab.reactor.parts

import fi.hacklab.reactor.parts.Part._

/**
 * 
 */

class SteamCondenser extends Part {

  val hotWaterIn = makePort(InFlow)
  val coolWaterIn = makePort(InFlow)
  val steamOut = makePort(OutFlow)
  val waterOut = makePort(OutFlow)


  def update(time_s: Double) {}
}