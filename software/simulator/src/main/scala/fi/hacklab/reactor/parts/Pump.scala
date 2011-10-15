package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives.Part

/**
 * Create a pressure gradient from the input to the output.
 */
class Pump extends Part {

  val in  = makePort()
  val out = makePort()

  def update(time_s: Double) {
    
  }

}