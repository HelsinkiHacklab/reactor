package fi.hacklab.reactor.parts

import org.scalaprops.Bean

/**
 * Some part of the reactor.
 */
trait Part extends Bean {

  private var ports: List[Port] = Nil


  def makePort(direction: Direction = InOutFlow): Port = {
    val port = new Port(this, direction)
    ports ::= port
    port
  }




  def preUpdate(time_s: Double) {}

  def update(time_s: Double)

  def postUpdate(time_s: Double) {}

}


trait Direction
case object InFlow extends Direction
case object OutFlow extends Direction
case object InOutFlow extends Direction
