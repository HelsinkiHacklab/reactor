package fi.hacklab.reactor.primitives

import org.scalaprops.Bean

/**
 * Some part of the reactor.
 */
// TODO: Outputs, signals in / out, sound generated, lights, etc
trait Part extends Bean {

  private var ports: List[Port] = Nil


  def makePort(direction: Direction = InOutFlow): Port = {
    addPort(new Port(this, direction))
  }

  def addPort(port: Port): Port = {
    ports ::= port
    port
  }



  def pressureUpdate(time_s: Double) {}

  def flowUpdate(time_s: Double) {}

  def update(time_s: Double)

  def postUpdate(time_s: Double) {}



  // TODO: associate these with ports somehow? onMatterAdded, etc?
  /**
   * Pressure at the specified port.
   */
  def getPressure(port: Port): Double = 0
  /**
   * Adds some matter from specified port
   */
  def addMatter(port: Port, matter: Matter) {}
  /**
   * Removes matter through specified port.
   */
  def removeMatterVolume(port: Port, volume_m3: Double): Matter = null


}

