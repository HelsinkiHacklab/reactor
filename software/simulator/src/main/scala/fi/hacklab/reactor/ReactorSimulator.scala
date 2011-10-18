package fi.hacklab.reactor

import org.scalaprops.Bean
import java.io.File
import primitives.{Simulator, Plant}

/**
 * 
 */
object ReactorSimulator {

  def main(args: Array[String]) {
    println("Helsinki Hacklab Reactor Simulator")

    // Get config
    println("  Getting configuration")
    val configFile: File = parseCommandLine(args)
    val config: Config = loadConfiguration(configFile)

    // Setup simulator
    println("  Initializing simulator")
    val simulator = new Simulator()
    simulator.registerUpdatePhase('preUpdate)
    simulator.registerUpdatePhase('update)
    simulator.registerUpdatePhase('postUpdate)

    // Create plant
    println("  Creating plant")
    val plant: Plant = PlantBuilder.build(config)
    plant.initialize(simulator)

    // And run forever
    println("  Starting simulation")
    simulator.run()
  }


  private def parseCommandLine(args: Array[String]): File = {
    if (args.length > 0) new File(args(0))
    else null
  }

  private def loadConfiguration(configFile: File): Config = {
    // Allow loading of config beans
    Bean.registerAcceptedBeanType(classOf[Config])

    // Default config
    var config: Config = new Config

    // If configuration file specified on command line, use or initialize it
    if (configFile != null) {
      if (configFile.exists()) {
        // Load config if found
        try {
          config = Bean.loadFromFile(configFile).asInstanceOf[Config]
        } catch {
          case e => println("Problem when loading configuration from file " + configFile + ": " + e.getMessage)
          exit(1)
        }
      }
      else {
        // If not found, save default config and use it
        println("Config file '" + configFile + "' doesn't exist, saving a default config file there and using it.")
        try {
          config.saveToFile(configFile)
        } catch {
          case e => println("Problem when saving configuration to file " + configFile + ": " + e.getMessage)
          exit(1)
        }
      }
    }

    config
  }

}