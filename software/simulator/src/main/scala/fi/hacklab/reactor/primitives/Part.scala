package fi.hacklab.reactor.primitives

import org.scalaprops.Bean

/**
 * Some part of the reactor.
 */
// TODO: Outputs, signals in / out, sound generated, lights, etc
trait Part extends Bean {

  private var ports: List[Port] = Nil


  def makePort(direction: Direction = InOutFlow): Port = {
    val port = new Port(this, direction)
    ports ::= port
    port
  }



  def pressureUpdate(time_s: Double) {}

  def flowUpdate(time_s: Double) {}

  def update(time_s: Double)

  def postUpdate(time_s: Double) {}


  /**
   * Pressure at the specified port.
   */
  def getPressure(port: Port): Double

  /**
   * Adds some matter from specified port
   */
  def addMatter(port: Port, matter: Matter)

  /**
   * Removes matter through specified port.
   */
  def removeMatterVolume(port: Port, volume_m3: Double): Matter


}

