package fi.hacklab.reactor.primitives

/**
 * Part consisting of many parts
 */
trait CompositePart extends Part {

  var parts: List[Part] = Nil

  def makePart(part: Part): Part = {
    parts ::= part
    part
  }

  final override def pressureUpdate(timeSeconds: Double) {
    parts foreach  {p => p.pressureUpdate(timeSeconds)}
    onPressureUpdate(timeSeconds)
  }

  final override def flowUpdate(timeSeconds: Double) {
    parts foreach  {p => p.flowUpdate(timeSeconds)}
    onFlowUpdate(timeSeconds)
  }

  final def update(timeSeconds: Double) {
    parts foreach  {p => p.update(timeSeconds)}
    onUpdate(timeSeconds)
  }


  final override def postUpdate(timeSeconds: Double) {
    parts foreach  {p => p.postUpdate(timeSeconds)}
    onPostUpdate(timeSeconds)
  }

  def onPressureUpdate(timeSeconds: Double) {}
  def onFlowUpdate(timeSeconds: Double) {}
  def onUpdate(timeSeconds: Double) {}
  def onPostUpdate(timeSeconds: Double) {}

}