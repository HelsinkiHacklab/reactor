package fi.hacklab.reactor.parts

/**
 * 
 */
case class Port(source: Container,
                target: Container,
                oneWay: Boolean = false,
                gasTransport: Boolean = true,
                liquidTransport: Boolean = true) extends Part {
  var flow_m3_per_s = 0.0


  def preUpdate(time_s: Double) {}
  def update(time_s: Double) {}
}

