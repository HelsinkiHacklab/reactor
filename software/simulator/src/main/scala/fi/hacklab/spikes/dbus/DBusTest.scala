package fi.hacklab.spikes.dbus

import org.freedesktop.DBus;
import org.freedesktop.dbus.DBusConnection;
import org.freedesktop.dbus.exceptions.DBusException;

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
  }

}