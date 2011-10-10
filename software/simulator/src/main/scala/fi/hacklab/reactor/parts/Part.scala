package fi.hacklab.reactor.parts

/**
 * Some part of the reactor.
 */
trait Part {

  def update(time_s: Double)

  def postUpdate(time_s: Double) {}

}