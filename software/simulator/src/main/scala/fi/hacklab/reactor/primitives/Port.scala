package fi.hacklab.reactor.primitives

/**
 * 
 */
case class Port(host: Part,
                direction: Direction,
                frictionCoefficient: Double = 0.1 ) extends Part {

  var pressure_Pa = 1.0

  // Connected pipe, if any.
  var connection: Connection = null

  def connectedPort : Port = {
    if (connection == null) null
    else if (connection.a == this) connection.b
    else connection.a
  }

  def disconnect() {
    disconnect(connection)
  }

  def disconnect(p: Connection) {
    if (p == connection && p != null) {
      connection = null;
      p.disconnect()
    }
  }

  def connect(connection: Connection) {
    if (connection != connection) {
      if (!connection.connectsToPort(this)) throw new IllegalArgumentException("Connection needs to connect to already connect to this port")

      disconnect()
      connection = connection
    }
  }

  def connect(otherPort: Port) {
    if (connectedPort != otherPort) {
      disconnect()

      connection = new Connection(this, otherPort)
      otherPort.connect(connection)
    }
  }



  // TODO: In update, check if we should move material out from this port (other connected ports will check if they should move material out of their ports and into ours)
  // TODO: How to do update cycles sensibly for ports & connections?


  override def pressureUpdate(time_s: Double) {
    // Calculate pressure
    pressure_Pa = host.getPressure(this)

  }

  override def flowUpdate(time_s: Double) {
    val otherPort = connectedPort
    if (otherPort != null && direction.allowsOut) {
      // Push to connected port, if applicable
      val pressureDifference = pressure_Pa - otherPort.pressure_Pa
      if (pressureDifference > 0) {
        val flow = connection.flow_m3_per_s + pressureDifference * (1.0 - frictionCoefficient)
      }
    }
  }


  def update(time_s: Double) {

  }
}

