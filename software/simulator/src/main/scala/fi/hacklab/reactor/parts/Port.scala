package fi.hacklab.reactor.parts

/**
 * 
 */
case class Port(host: Part,
                direction: Direction) extends Part {
  var flow_m3_per_s = 0.0

  // Connected pipe, if any.
  var pipe: Pipe = null

  def connectedPort : Port = {
    if (pipe == null) null
    else if (pipe.a == this) pipe.b
    else pipe.a
  }

  def disconnect() {
    disconnect(pipe)
  }

  def disconnect(p: Pipe) {
    if (p == pipe && p != null) {
      pipe = null;
      p.disconnect()
    }
  }

  def connect(connection: Pipe) {
    if (pipe != connection) {
      if (!connection.connectsToPort(this)) throw new IllegalArgumentException("Connection needs to connect to already connect to this port")

      disconnect()
      pipe = connection
    }
  }

  def connect(otherPort: Port) {
    if (connectedPort != otherPort) {
      disconnect()

      pipe = new Pipe(this, otherPort)
      otherPort.connect(pipe)
    }
  }

  // TODO: In update, check if we should move material out from this port (other connected ports will check if they should move material out of their ports and into ours)
  // TODO: How to do update cycles sensibly for ports & connections?

  override def preUpdate(time_s: Double) {}
  def update(time_s: Double) {}
}

