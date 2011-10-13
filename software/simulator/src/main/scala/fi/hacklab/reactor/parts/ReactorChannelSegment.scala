package fi.hacklab.reactor.parts

/**
 * A segment of a reactor channel.
 */
class ReactorChannelSegment(x: Int, y: Int, z: Int, reactorChannel: ReactorChannel) extends Part {

  var temperature = 0.0
  var neutronActivity = 0.0
  var neutronFluxOut = 0.0
  var neutronFluxIn = 0.0
  var waterChannel: Container = new Container
  var surroundingSegments: List[ReactorChannelSegment] = Nil

  override def preUpdate(time_s: Double) {
    waterChannel.preUpdate(time_s)
  }

  def update(time_s: Double) {
    waterChannel.update(time_s)

    // Calculate the incoming flux, based on outgoing flux by other channels, and control rod and water positions

    // Update activity based on incoming flux

    // Calculate the temperature based on activity and cooling flow

  }

  override def postUpdate(time_s: Double) {
    waterChannel.postUpdate(time_s)

    // Calculate the outgoing flux

  }


}