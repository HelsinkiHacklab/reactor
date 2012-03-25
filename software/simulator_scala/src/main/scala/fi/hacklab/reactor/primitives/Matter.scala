package fi.hacklab.reactor.primitives

/**
 * 
 */
class Matter {

  def mass_kg = water_kg + steam_kg
  var temperature_K = 0.0

  var water_kg = 0.0
  var steam_kg = 0.0

  def neutronAbsorbation: Double = 0

  def add(other: Matter) {
    water_kg += other.water_kg
    steam_kg += other.steam_kg
  }

  def remove(mass_kg: Double): Matter = {
    val part = math.min(1, mass_kg / this.mass_kg)

    val result = new Matter()
    result.water_kg = water_kg * part
    result.steam_kg = steam_kg * part

    water_kg -= result.water_kg
    steam_kg -= result.steam_kg

    result
  }
}