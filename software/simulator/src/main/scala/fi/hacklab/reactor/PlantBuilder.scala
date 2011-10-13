package fi.hacklab.reactor

import parts.{Reactor, ReactorChannelSegment, ReactorChannel, Plant}

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