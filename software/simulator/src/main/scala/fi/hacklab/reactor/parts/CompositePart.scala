package fi.hacklab.reactor.parts

/**
 * Part consisting of many parts
 */
trait CompositePart extends Part {

  var parts: List[Part] = Nil

  def addPart(part: Part) {
    parts ::= part
  }

  final override def preUpdate(timeSeconds: Double) {
    parts foreach  {p => p.preUpdate(timeSeconds)}
    onPreUpdate(timeSeconds)
  }

  final def update(timeSeconds: Double) {
    parts foreach  {p => p.update(timeSeconds)}
    onUpdate(timeSeconds)
  }


  final override def postUpdate(timeSeconds: Double) {
    parts foreach  {p => p.postUpdate(timeSeconds)}
    onPostUpdate(timeSeconds)
  }

  def onPreUpdate(timeSeconds: Double) {}
  def onUpdate(timeSeconds: Double) {}
  def onPostUpdate(timeSeconds: Double) {}

}