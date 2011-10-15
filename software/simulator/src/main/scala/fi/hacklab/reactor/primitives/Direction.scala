package fi.hacklab.reactor.primitives

class Direction(val allowsOut: Boolean, val allowsIn: Boolean)

case object InFlow extends Direction(false, true)
case object OutFlow extends Direction(true, false)
case object InOutFlow extends Direction(true, true)

