package fi.hacklab.reactor.parts

/**
 * A fluid pipe or cistern, with connections to other ones.
 */
class Container extends Part {

  var volume = 1.0
  var surfaceArea = 1.0
  var heatTransferCoefficient = 0.8

  val water = new Fluid
  val steam = new Fluid
  val hydrogen = new Fluid
  val oxygen = new Fluid

  var ports: List[Port] = Nil

  var pressure = 0.0

  def neutronAbsorbation: Double = water.amountKg // TODO

  def heatExchange(time_s: Double, outerTemperature_K: Double) {
    // Average own and outer temperature, based on surface area and heat transfer coefficient
  }

  def update(time_s: Double) {
    // Calculate pressure based on amount of matter and heat
    // Convert water to steam or steam to water based on temperature and pressure
    // Convert steam to hydrogen and oxygen if it is too hot
  }

  def postUpdate(time_s: Double) {
    // Update flow of matter from and to openings, based on relative pressures, and on what materials can pass
    // through each port in which direction
  }

}

case class Port(host: Container, portType: PortType, gas: Boolean, liquid: Boolean) {
  var flow_m3_per_s = 0.0
}

sealed trait PortType
case object InPort extends PortType
case object OutPort extends PortType
case object InOutPort extends PortType
