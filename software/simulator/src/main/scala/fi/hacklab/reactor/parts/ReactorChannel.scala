package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives.CompositePart

/**
 * 
 */
case class ReactorChannel(posX: Int, posY: Int, sizeZ: Int, reactor: Reactor) extends CompositePart {

  initSegments()

  var controlRodPosition = 0.0
  var controlRodFromTop = true

  private def initSegments() {
    // Make channel segments
    for (z <- 0 until sizeZ) {
      val segment = new ReactorChannelSegment(posX, posY, z, this)
      reactor.segmentLookup += (posX, posY, z) -> segment
    }
  }

}