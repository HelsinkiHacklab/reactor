package fi.hacklab.reactor

import parts._
import primitives.{Simulator, Plant}

/**
 * Builds the plant
 */
object PlantBuilder {

  def build(config: Config): Plant = {


    val plant = new Plant()

    // TODO

    plant.addRoom('reactorRoom)

    // Reactor rods and channels
    val reactor = plant.addPart(new Reactor(
      config.reactorSegmentsX(),
      config.reactorSegmentsY(),
      config.reactorSegmentsZ(),
      config.reactorSegmentsCutout()))
    plant.addPart(reactor)

    plant.addRoom('steamSeparatorRoom)

    // Steam separators
    val steamSeparator1 = plant.addPart(new SteamCondenser())
    val steamSeparator2 = plant.addPart(new SteamCondenser())

    reactor.hotWaterOut1 connect steamSeparator1.hotWaterIn
    reactor.hotWaterOut2 connect steamSeparator2.hotWaterIn

    val steamPipe = plant.addPart(new Branch())

    steamSeparator1.steamOut connect steamPipe.left
    steamSeparator2.steamOut connect steamPipe.right

    // Vent to bubbler pools / out
    val emergencySteamVent = plant.addPart(new Valve())
    
    emergencySteamVent.a connect steamPipe.back

    plant.addRoom('electricityRoom)
    // Turbines

    val turbine1 = plant.addPart(new Turbine())
    val turbine2 = plant.addPart(new Turbine())
    steamPipe.up connect turbine1.steamIn
    steamPipe.down connect turbine2.steamIn

    // (Generators (simulate separately later))

    // Diesel generator

    // Energy output

    // External energy input

    plant.addRoom('waterIntake)

    // River water intake, pumps, outlet

    plant.addRoom('coolerRoom)

    // Heat exchanger

    // Cooling water storage tanks

    // Cooling water pumps

    plant.addRoom('reactorPumpRoom)
    // Main reactor circulation pumps
    val mainPump1 = plant.addPart(new Pump())
    val mainPump2 = plant.addPart(new Pump())
    val mainPump3 = plant.addPart(new Pump())
    val mainPump4 = plant.addPart(new Pump())

    val branch1 = plant.addPart(new TBranch())
    val branch2 = plant.addPart(new TBranch())

    steamSeparator1.waterOut connect branch1.a
    steamSeparator2.waterOut connect branch2.a

    branch1.b connect mainPump1.in
    branch1.c connect mainPump2.in
    branch2.b connect mainPump3.in
    branch2.c connect mainPump4.in

    mainPump1.out connect reactor.coolingWaterIntake1
    mainPump2.out connect reactor.coolingWaterIntake2
    mainPump3.out connect reactor.coolingWaterIntake3
    mainPump4.out connect reactor.coolingWaterIntake4

    // Emergency pump


    plant
  }

}