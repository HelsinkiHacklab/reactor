package fi.hacklab.reactor.parts

/**
 * 
 */
case class ReactorChannel() extends Part {

  class PosData {
    var temperature = 0.0
    var neutronActivity = 0.0
    var neutronFluxOut = 0.0
    var waterChannel: Container = new Container
  }

  var conditionsAtHeight: List[PosData] = Nil

  def update(time_s: Double) {
    // Update activity based on natural activity and own and incoming flux, blocked by control rods and liquid water

    // Calculate the outgoing flux

    // Calculate the temperature based on activity and cooling flow
  }


}