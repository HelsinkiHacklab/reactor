import QtQuick 1.0

Rectangle
{
    id: rodSwitches
    width: parent.width; height: parent.height
    // Rows
    // TODO: change the "pins" to the indices mapped in simple_servo_control.py
    Column
    {
        width: parent.width; height: parent.height
        // Row 1
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo0"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo1"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo2"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
            }
        }

        // Row 2
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo3"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorLed
                    {
                        ledColor: "white"
                        objectName: "rodled0"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo4"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo5"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo6"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
            }
        }

        // Row 3
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo7"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo8"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo9"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo10"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo11"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorLed
                    {
                        ledColor: "white"
                        objectName: "rodled2"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo13"
                    }
                }
            }
        }

        // Row 4
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo14"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo15"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo16"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo17"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo18"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo19"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo20"
                    }
                }
            }
        }

        // Row 5
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo21"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorLed
                    {
                        ledColor: "white"
                        objectName: "rodled2"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo22"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo23"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo24"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo25"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo26"
                    }
                }
            }
        }

        // Row 6
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo27"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo28"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo29"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorLed
                    {
                        ledColor: "white"
                        objectName: "rodled3"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo30"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
            }
        }

        // Row 7
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo31"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo32"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorGauge
                    {
                        objectName: "arduino0_servo33"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
            }
        }
    // End column
    }
}