package fi.hacklab.reactor.primitives

import fi.hacklab.reactor.primitives.Part

/**
 * 
 */
class Plant {

  var parts: List[Part] = Nil
  
  def addPart(part: Part) {
    parts ::= part
  }

  def update(time_s: Double) {
    parts foreach {p => p.pressureUpdate(time_s)}
    parts foreach {p => p.flowUpdate(time_s)}
    parts foreach {p => p.update(time_s)}
    parts foreach {p => p.postUpdate(time_s)}
  }

  def run() {
    // TODO?
  }


}