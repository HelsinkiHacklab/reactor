package fi.hacklab.reactor.primitives

/**
 * 
 */
class Plant extends CompositePart {

  var rooms: List[Room] = Nil

  private var currentRoom: Room = null

  /**
   * Adds new room, also sets it to the current room, that any added parts are located in.
   */
  def addRoom(name: Symbol): Room = {
    val room = new Room(name)
    rooms ::= room
    setCurrentRoom(room)
    room
  }

  def setCurrentRoom(room: Room) {currentRoom = room}

  override def onPartAdded(part: Part) {
    if (currentRoom != null) currentRoom.addPart(part)
  }
}
