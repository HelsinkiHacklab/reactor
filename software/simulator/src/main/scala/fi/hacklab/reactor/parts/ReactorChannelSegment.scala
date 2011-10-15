package fi.hacklab.reactor.parts

import fi.hacklab.reactor.primitives.{CompositePart, Container, Part}

/**
 * A segment of a reactor channel.
 */
class ReactorChannelSegment(x: Int, y: Int, z: Int, reactorChannel: ReactorChannel) extends CompositePart {

  var temperature = 0.0
  var neutronActivity = 0.0
  var neutronFluxOut = 0.0
  var neutronFluxIn = 0.0

  var waterChannel: Container = makePart(new Container)


  def onUpdate(time_s: Double) {

    // Calculate the incoming flux, based on outgoing flux by other channels, and control rod and water positions

    // Update activity based on incoming flux

    // Calculate the temperature based on activity and cooling flow

  }

  def onPostUpdate(time_s: Double) {
    // Calculate the outgoing flux

  }


}