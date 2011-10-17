package fi.hacklab.reactor

import parts._
import primitives.Plant

/**
 * Builds the plant
 */
object PlantBuilder {

  def build(config: Config): Plant = {

    val plant = new Plant()

    // TODO

    // Reactor rods and channels

    val reactor = new Reactor(
      config.reactorSegmentsX(),
      config.reactorSegmentsY(),
      config.reactorSegmentsZ(),
      config.reactorSegmentsCutout())
    plant.addPart(reactor)

    // Steam separators
    val steamSeparator1 = new SteamCondenser()
    val steamSeparator2 = new SteamCondenser()

    reactor.hotWaterOut1 connect steamSeparator1.hotWaterIn
    reactor.hotWaterOut2 connect steamSeparator2.hotWaterIn

    // Turbines

    // Generators

    // Heat exchanger

    // River water intake, pumps, outlet

    // Cooling water storage tanks

    // Cooling water pumps

    // Main reactor circulation pumps

    // Emergency pump

    // Diesel generators

    // Energy output

    // External energy input

    // Vent to bubbler pools


    plant
  }

}