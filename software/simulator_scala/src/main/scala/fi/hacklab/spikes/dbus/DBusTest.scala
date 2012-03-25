package fi.hacklab.spikes.dbus

import org.freedesktop.DBus;

import org.freedesktop.dbus.exceptions.DBusException
import org.freedesktop.dbus.{DBusInterface, DBusSignal, DBusSigHandler, DBusConnection}
;

;

/**
 * 
 */

object DBusTest  {



  def main(args: Array[ String ]) {

    var conn: DBusConnection  = null
        System.out.println("Creating DBus Connection")

        try {
          conn = DBusConnection.getConnection(DBusConnection.SYSTEM)
        } catch {
          case e => println("Could not connect to bus: " + e)
                    System.exit(1)

        }

        System.out.println("Created")


      val handler = new DBusSigHandler[ReactorInterface#control_rod_up] {
          def handle(s: ReactorInterface#control_rod_up) {
            println(s.getName)
            println(s)
          }
        }

//        conn.addSigHandler(classOf[ReactorInterface#control_rod_up], handler)

        conn.addSigHandler(classOf[ReactorInterface#control_rod_up], "", handler)

//        conn.sendSignal(new DBusSignal())

  }




  trait ReactorInterface extends DBusInterface {

    class control_rod_up(val path: String, val number: Int, val state: Boolean) extends DBusSignal(path, number.asInstanceOf[java.lang.Integer], state.asInstanceOf[java.lang.Boolean])
    class control_rod_down(val path: String, val number: Int, val state: Boolean) extends DBusSignal(path, number.asInstanceOf[java.lang.Integer], state.asInstanceOf[java.lang.Boolean])

  }

}