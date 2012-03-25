package fi.hacklab.reactor.primitives.hifimodel

/**
 * 
 */

trait Processor {

  def process(storage: Storage, time: Double)

}
