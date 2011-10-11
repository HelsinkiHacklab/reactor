package fi.hacklab.reactor.parts

/**
 * 
 */
case class ReactorChannel() extends Part {

  class PosData {
    var temperature = 0.0
    var neutronActivity = 0.0
    var neutronFluxOut = 0.0
    var neutronFluxIn = 0.0
    var waterChannel: Container = new Container
  }

  var conditionsAtHeight: List[PosData] = Nil

  def update(time_s: Double) {
    // Calculate the incoming flux, based on outgoing flux by other channels, and control rod and water positions

    // Update activity based on incoming flux

    // Calculate the temperature based on activity and cooling flow
  }


  override def postUpdate(time_s: Double) {

    // Calculate the outgoing flux

  }
}