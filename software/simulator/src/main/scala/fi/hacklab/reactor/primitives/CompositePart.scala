package fi.hacklab.reactor.primitives

import java.util.HashSet

/**
 * Part consisting of many parts
 */
trait CompositePart extends Part {

  var parts: List[Part] = Nil

  // TODO: exportPort method that stores info about exported ports from contained parts?

  /**
   * Delegates to init methods in components.
   */
  final override def initialize(simulator: Simulator) {
    parts foreach (p => p.initialize(simulator))

    super.initialize(simulator)
  }


  def addPart[T <: Part](part: T): T = {
    parts ::= part
    part
  }

  protected def collectConnectedParts(connectedParts: HashSet[Part]) {
    if (!connectedParts.contains(this)) {
      super.collectConnectedParts(connectedParts)
      parts foreach {p => p.collectConnectedParts(connectedParts)}
    }
  }

}