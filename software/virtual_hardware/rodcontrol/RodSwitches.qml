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
                        upPin: 18
                        downPin: 17
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 24
                        downPin: 39
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 34
                        downPin: 50
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
                        upPin: 33
                        downPin: 3
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
                        upPin: 30
                        downPin: 43
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 32
                        downPin: 38
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 20
                        downPin: 35
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
                        upPin: 23
                        downPin: 2
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 31
                        downPin: 4
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 22
                        downPin: 36
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 27
                        downPin: 0
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 28
                        downPin: 5
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
                        upPin: 61
                        downPin: 12
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
                        upPin: 64
                        downPin: 7
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 52
                        downPin: -1
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 19
                        downPin: 47
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 21
                        downPin: 13
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 26
                        downPin: 49
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 25
                        downPin: 14
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 60
                        downPin: 42
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
                        upPin: 54
                        downPin: 15
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
                        upPin: 66
                        downPin: 6
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 65
                        downPin: 40
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 63
                        downPin: 46
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 59
                        downPin: 44
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 62
                        downPin: 1
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
                        upPin: 55
                        downPin: 16
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 53
                        downPin: 41
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    Reactor3Switch
                    {
                        upPin: 58
                        downPin: 8
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
                        upPin: 56
                        downPin: 11
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
                        upPin: 57
                        downPin: 9
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