import sbt._
import com.github.retronym.OneJarProject

class Project(info: ProjectInfo) extends DefaultProject(info) with IdeaProject with OneJarProject {

//  override def mainClass = Some("org.foo.MainObj")

  // Scala unit testing
  val scalatest = "org.scalatest" % "scalatest" % "1.3"

}
