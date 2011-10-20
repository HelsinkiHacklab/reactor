package fi.hacklab.reactor.primitives

/**
 * A room in the reactor where some equipment can be located.
 * Has some technicians allocated, that will try to fix problems.
 */
case class Room(name: Symbol, var technicianCount: Int = 3) {

  private var parts: List[Part] = Nil

  def addPart(part: Part) {
    parts ::= part
  }

}
