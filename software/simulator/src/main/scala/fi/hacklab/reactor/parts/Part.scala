package fi.hacklab.reactor.parts

import org.scalaprops.Bean

/**
 * Some part of the reactor.
 */
trait Part extends Bean {

  def preUpdate(time_s: Double) {}

  def update(time_s: Double)

  def postUpdate(time_s: Double) {}

}