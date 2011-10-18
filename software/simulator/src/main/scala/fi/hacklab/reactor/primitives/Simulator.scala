package fi.hacklab.reactor.primitives

import collection.mutable.LinkedHashMap
import java.util.{ArrayList, HashSet}
import scala.collection.JavaConversions._

/**
 * Takes care of all update calling.
 */
class Simulator {

  private val updatePhases = new LinkedHashMap[Symbol, ArrayList[(Double) => Unit]]()
  private var previousTime_ms: Long = 0

  var timeScale = 1.0

  def registerUpdatePhase(name: Symbol) {
    updatePhases.put(name, new ArrayList[(Double) => Unit]())
  }

  def addUpdate(phase: Symbol)(updateFunction: (Double) => Unit) {
    updatePhases.get(phase) match {
      case None => throw new IllegalArgumentException("Unknown update phase: " + phase.name)
      case Some(updateFunctions) => updateFunctions.add(updateFunction)
    }
  }

  def update(time_s: Double) {
    updatePhases.values foreach { updateFunctions: ArrayList[(Double) => Unit] =>
      updateFunctions foreach {(uf: (Double) => Unit) => uf(time_s) }
    }
  }

  def run() {
    while (true) {

      if (previousTime_ms == 0) {
        previousTime_ms = System.currentTimeMillis()
      }
      else {
        val time_ms = System.currentTimeMillis()
        val duration_ms = time_ms - previousTime_ms
        if (duration_ms > 0) {
          val duration_s = 0.001 * duration_ms * timeScale
          update(duration_s)
        }
      }

      Thread.`yield`() // Workaround to call yield named Java function, as it is reserved word in Scala.
    }
  }


}