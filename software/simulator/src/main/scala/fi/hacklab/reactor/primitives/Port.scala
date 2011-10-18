package fi.hacklab.reactor.primitives

/**
 * 
 */

trait Port {

  def host: Part

  private var _connectedPort: Port = null

  def connectedPort[T <: Port]: T = _connectedPort.asInstanceOf[T]

  def kind: Symbol = Symbol(getClass.getSimpleName)

  def init(simulator: Simulator)

  def disconnect() {
    if (_connectedPort != null) {
      val c = _connectedPort
      _connectedPort = null
      c.disconnect()
    }
  }

  def connect(otherPort: Port) {
    if (otherPort != _connectedPort) {
      if (otherPort == null) throw new IllegalArgumentException("Can't connect to null")
      if (otherPort == this) throw new IllegalArgumentException("Can't connect to self")
      if (otherPort.kind != kind) throw new IllegalArgumentException("Can't connect a "+kind.name+" port to a " + otherPort.kind.name + " port")

      disconnect()

      _connectedPort = otherPort
      otherPort.connect(this)
    }
  }


}