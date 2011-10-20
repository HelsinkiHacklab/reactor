package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives.{Simulator, FluidPort, CompositePart}

/**
 * 
 */

class Reactor(sizeX: Int, sizeY: Int, sizeZ: Int, edgeCutoutSize: Int) extends CompositePart {



  
  var coolingWaterIntake1: FluidPort = null
  var coolingWaterIntake2: FluidPort = null
  var coolingWaterIntake3: FluidPort = null
  var coolingWaterIntake4: FluidPort = null
  var hotWaterOut1: FluidPort = null
  var hotWaterOut2: FluidPort = null


  var segmentLookup = Map[(Int,Int,Int), ReactorChannelSegment]()

  private var channelLookup = Map[(Int,Int), ReactorChannel]()
  private var topPipeLookup = Map[(Int,Int), Branch]()
  private var bottomPipeLookup = Map[(Int,Int), Branch]()

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

  def channel(x: Int, y: Int): ReactorChannel = {
    if (hasChannel(x, y)) channelLookup((x, y))
    else null
  }

  private def initChannels() {
    for (x <- 0 until sizeX;
         y <- 0 until sizeY) {

      if (hasChannel(x, y)) {
        val topPipe: Branch = addPart(new Branch())
        topPipeLookup += (x, y) -> topPipe

        val bottomPipe: Branch = addPart(new Branch())
        bottomPipeLookup += (x, y) -> bottomPipe

        val channel = addPart(new ReactorChannel(x, y, sizeZ, this))
        channelLookup += (x, y) -> channel
      }

    }

    // Build lattice of pipes above and under
    for (x <- 0 until sizeX;
         y <- 0 until sizeY) {

      if (hasChannel(x, y)) {

        // Top
        val topBranch: Branch = topPipeLookup((x, y))
        channel(x, y).topPort connect topBranch.down

        if (hasChannel(x + 1, y)) topBranch.right connect topPipeLookup((x + 1, y)).left
        if (hasChannel(x, y + 1)) topBranch.forward connect topPipeLookup((x, y + 1)).back

        // Bottom
        val bottomBranch: Branch = bottomPipeLookup((x, y))
        channel(x, y).bottomPort connect bottomBranch.up

        if (hasChannel(x + 1, y)) bottomBranch.right connect bottomPipeLookup((x + 1, y)).left
        if (hasChannel(x, y + 1)) bottomBranch.forward connect bottomPipeLookup((x, y + 1)).back

      }
    }

    // Get external connection points
    // TODO: Connect top at middle left right, bottom maybe at corners?

  }

}


