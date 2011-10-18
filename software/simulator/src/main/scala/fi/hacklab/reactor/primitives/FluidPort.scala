package fi.hacklab.reactor.primitives

/**
 * 
 */
class FluidPort(val host: Part,
                val direction: Direction,
                pressure: () => Double,
                addMatter: (Matter) => Unit,
                removeMatter_m3: (Double) => Matter,
                frictionCoefficient: Double = 0.1 ) extends Port {

  var pressure_Pa = 1.0
  var outFlow_m3_per_s = 0





  // TODO: In update, check if we should move material out from this port (other connected ports will check if they should move material out of their ports and into ours)
  // TODO: How to do update cycles sensibly for ports & connections?


  def init(simulator: Simulator) {
    // TODO: Move updates here
  }

  override def pressureUpdate(time_s: Double) {
    // Calculate pressure
    pressure_Pa = pressure()

  }

  override def flowUpdate(time_s: Double) {
    val otherPort = connectedPort[FluidPort]
    if (otherPort != null && direction.allowsOut && otherPort.direction.allowsIn) {
      val pressureDifference = pressure_Pa - otherPort.pressure_Pa
      if (pressureDifference > 0) {
        outFlow_m3_per_s = outFlow_m3_per_s + pressureDifference - outFlow_m3_per_s * outFlow_m3_per_s * frictionCoefficient
        if (outFlow_m3_per_s < 0) outFlow_m3_per_s = 0
      }
      else outFlow_m3_per_s = 0
    }
    else outFlow_m3_per_s = 0
  }


  def update(time_s: Double) {
    // Push matter to connected port, if there is flow
    if (outFlow_m3_per_s > 0) {
      val volume = outFlow_m3_per_s * time_s
      val matter = removeMatter_m3(volume)
      addMatter(matter)
    }
  }



}

