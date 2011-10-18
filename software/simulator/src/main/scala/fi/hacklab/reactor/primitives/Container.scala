package fi.hacklab.reactor.primitives

/**
 * A fluid pipe or cistern, with connections to other ones.
 */
class Container(var volume: Double = 1.0) extends Part {

  var surfaceArea = 1.0
  var heatTransferCoefficient = 0.8

  val matter = new Matter

  var ports: List[FluidPort] = Nil

  var pressure = 0.0

  def fluidPort(direction: Direction = InOutFlow,
                frictionCoefficient: Double = 0.01): FluidPort = {
    fluidPort(direction, () => pressure, frictionCoefficient)
  }

  def fluidPort(direction: Direction,
                pressureFunc:  () => Double): FluidPort = {
    fluidPort(direction, pressureFunc, 0.1)
  }

  def fluidPort(direction: Direction,
                pressureFunc:  () => Double,
                frictionCoefficient: Double): FluidPort = {
    addPort(new FluidPort(this, direction, pressureFunc, addMatter, removeMatterVolume, frictionCoefficient))
  }


  def density: Double = matter.mass_kg / volume

  def neutronAbsorbation: Double = matter.neutronAbsorbation // TODO

  def heatExchange(time_s: Double, outerTemperature_K: Double) {
    // Average own and outer temperature, based on surface area and heat transfer coefficient
  }

  private def update(time_s: Double) {
    pressure = 0  // TODO: Calculate from compressibility of matter + elasticity of walls.

    // Calculate pressure based on amount of matter and heat
    // Convert water to steam or steam to water based on temperature and pressure
    // Convert steam to hydrogen and oxygen if it is too hot

    // Check for bursting
  }

  private def postUpdate(time_s: Double) {
    // Update flow of matter from and to openings, based on relative pressures, and on what materials can pass
    // through each port in which direction
  }


  def addMatter(matter: Matter) {
    this.matter.add(matter)
  }

  def removeMatterVolume(volume_m3: Double): Matter = {
    val mass = density * volume_m3
    matter.remove(mass)
  }
}
