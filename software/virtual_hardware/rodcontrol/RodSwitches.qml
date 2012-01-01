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
                    Reactor3Switch
                    {
                        upPin: 1
                        downPin: 2
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 3
                        downPin: 4
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 5
                        downPin: 6
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
                    Reactor3Switch
                    {
                        upPin: 7
                        downPin: 8
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
                    Reactor3Switch
                    {
                        upPin: 11
                        downPin: 12
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 13
                        downPin: 14
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 15
                        downPin: 16
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
                    Reactor3Switch
                    {
                        upPin: 17
                        downPin: 18
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 19
                        downPin: 20
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 21
                        downPin: 22
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 23
                        downPin: 24
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 25
                        downPin: 26
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorLed
                    {
                        ledColor: "white"
                        objectName: "rodled1"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 29
                        downPin: 30
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
                    Reactor3Switch
                    {
                        upPin: 31
                        downPin: 32
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 33
                        downPin: 34
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 35
                        downPin: 36
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 37
                        downPin: 38
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 39
                        downPin: 40
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 41
                        downPin: 42
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 43
                        downPin: 44
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
                    Reactor3Switch
                    {
                        upPin: 45
                        downPin: 46
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
                    Reactor3Switch
                    {
                        upPin: 49
                        downPin: 50
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 51
                        downPin: 52
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 53
                        downPin: 54
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 44
                        downPin: 56
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 57
                        downPin: 58
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
                    Reactor3Switch
                    {
                        upPin: 59
                        downPin: 60
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 61
                        downPin: 62
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 63
                        downPin: 64
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
                    Reactor3Switch
                    {
                        upPin: 67
                        downPin: 68
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
                    Reactor3Switch
                    {
                        upPin: 69
                        downPin: 70
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 71
                        downPin: 72
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 73
                        downPin: 74
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