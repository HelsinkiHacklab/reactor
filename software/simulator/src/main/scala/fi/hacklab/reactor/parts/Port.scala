package fi.hacklab.reactor.parts

/**
 * 
 */
case class Port(host: Container,
                oneWay: Boolean = false,
                gasTransport: Boolean = true,
                liquidTransport: Boolean = true) extends Part {
  var flow_m3_per_s = 0.0

  // Connected pipe, if any.
  var pipe: Pipe = null

  override def preUpdate(time_s: Double) {}
  def update(time_s: Double) {}
}

