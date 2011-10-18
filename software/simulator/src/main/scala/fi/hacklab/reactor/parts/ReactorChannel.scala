package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives.{FluidPort, CompositePart}

/**
 * 
 */
case class ReactorChannel(posX: Int, posY: Int, sizeZ: Int, reactor: Reactor) extends CompositePart {

  initSegments()

  var controlRodPosition = 0.0
  var controlRodFromTop = true

  var topPort:    FluidPort = null
  var bottomPort: FluidPort = null

  private def initSegments() {
    // Make channel segments
    for (z <- 0 until sizeZ) {
      val segment = new ReactorChannelSegment(posX, posY, z, this)
      reactor.segmentLookup += (posX, posY, z) -> segment
    }

    // Connect them
    for (z <- 1 until sizeZ) {
      val below = reactor.segment(posX, posY, z - 1)
      val above = reactor.segment(posX, posY, z)

      below.topPort connect above.bottomPort
    }

    // Get outside ports
    topPort = reactor.segment(posX, posY, sizeZ - 1).topPort
    bottomPort = reactor.segment(posX, posY, 0).bottomPort
  }

}