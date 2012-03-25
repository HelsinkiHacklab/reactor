package fi.hacklab.reactor.primitives

import org.scalaprops.Bean
import java.util.HashSet
import scala.collection.JavaConversions._

/**
 * Some part of the reactor.
 */
// TODO: Outputs, signals in / out, sound generated, lights, etc
trait Part extends Bean {

  private var ports: List[Port] = Nil


  /**
   * Delegates to init methods in class.
   */
  def initialize(simulator: Simulator) {
    ports foreach {p => p.init(simulator)}
    init(simulator)
  }

  /**
   * Called to allow part to set up any update functions.
   */
  protected def init(simulator: Simulator)



  def addPort[T <: Port](port: T): T = {
    ports ::= port
    port
  }


  final def collectConnectedParts(): HashSet[Part] = {
    val set: HashSet[Part] = new HashSet[Part]()
    collectConnectedParts(set)
    set
  }

  def collectConnectedParts(connectedParts: HashSet[Part]) {
    if (!connectedParts.contains(this)) {
      connectedParts add this

      ports foreach {p =>
        if (p.connectedPort != null) p.connectedPort.host.collectConnectedParts(connectedParts)
      }
    }
  }



}

