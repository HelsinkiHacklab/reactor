package fi.hacklab.reactor

import org.scalaprops.Bean

/**
 * 
 */
class Config extends Bean {

  val reactorHeight_m = p('reactorHeight_m, 1.0)

  val reactorSegmentsX = p('reactorSegmentsX, 7)
  val reactorSegmentsY = p('reactorSegmentsY, 7)
  val reactorSegmentsZ = p('reactorSegmentsZ, 7)
  val reactorSegmentsCutout = p('reactorSegmentsCutout, 2)

  val waterChannelRadius_m = p('waterChannelRadius_m, 0.025)
  val activityLevel = p('activityLevel, 1.0)
  val activityLevelVariation = p('activityLevelVariation, 0.3)

  val controlRodGraphiteTipPortion = p('controlRodGraphiteTipPortion, 0.2)
  val controlRodNeutronAbsorbation = p('controlRodNeutronAbsorbation, 1.0)
  var controlRodTipNeutronSlowdown = p('controlRodTipNeutronSlowdown, 1.0)

}