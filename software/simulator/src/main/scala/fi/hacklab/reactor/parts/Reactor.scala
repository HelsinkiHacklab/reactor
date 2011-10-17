package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives.CompositePart


/**
 * 
 */

class Reactor(sizeX: Int, sizeY: Int, sizeZ: Int, edgeCutoutSize: Int) extends CompositePart {

  val coolingWaterIntake1 = makePort()
  val coolingWaterIntake2 = makePort()
  val hotWaterOut1 = makePort()
  val hotWaterOut2 = makePort()


  private var channels: List[ReactorChannel] = Nil
  var segmentLookup = Map[(Int,Int,Int), ReactorChannelSegment]()

  initChannels()

  def hasChannel(x: Int, y: Int): Boolean = {
    def edge(a: Int, b: Int): Boolean = a + b < edgeCutoutSize

    if (x < 0 ||
        y < 0 ||
        x >= sizeX ||
        y >= sizeY) false
    else if (edge(x, y) ||
             edge(sizeX - x, y) ||
             edge(x, sizeY - y) ||
             edge(sizeX - x, sizeY - y)) false
    else true
  }

  def hasSegment(x: Int, y: Int, z: Int): Boolean = {
    hasChannel(x, y) &&  z >= 0 && z < sizeZ
  }

  def segment(x: Int, y: Int, z: Int): ReactorChannelSegment = {
    if (hasSegment(x, y, z)) segmentLookup((x, y, z))
    else null
  }

  private def initChannels() {
    for (x <- 0 until sizeX;
         y <- 0 until sizeY) {

      if (hasChannel(x, y)) {
        val channel = new ReactorChannel(x, y, sizeZ, this)
        addPart(channel)
        channels ::= channel
      }
    }

  }

}


