import com.typesafe.sbt.SbtNativePackager.packageArchetype

enablePlugins(JavaServerAppPackaging)

name := "common"

organization := "org.tellerum"

version := "0.1.0"

scalaVersion := "2.11.6"

scalacOptions ++= Seq("-feature")

resolvers += "Typesafe Repository" at "http://repo.typesafe.com/typesafe/releases/"

resolvers += "spray repo" at "http://repo.spray.io"

resolvers ++= Seq("snapshots", "releases").map(Resolver.sonatypeRepo)

resolvers += Resolver.mavenLocal

packageDescription := "A longer description of your application"

rpmVendor := "Tellerum"

dockerRepository := Some("tutum.co/tellerum")

val akka = "2.3.10"
val spray = "1.3.3"

libraryDependencies ++= Seq()

javaOptions := Seq("-Xdebug", "-Xrunjdwp:transport=dt_socket,server=n,suspend=y,address=5005")

mainClass := Some("tellerum.example.Boot")

mainClass in Revolver.reStart := Some("tellerum.example.Boot")

mainClass in run := Some("tellerum.example.Boot")

mainClass in Compile := Some("tellerum.example.Boot")

javacOptions ++= Seq("-source", "1.8", "-target", "1.8", "-Xlint")

initialize := {
    val _ = initialize.value
    if (sys.props("java.specification.version") != "1.8")
        sys.error("Java 8 is required for this project.")
}

seq(Revolver.settings: _*)
