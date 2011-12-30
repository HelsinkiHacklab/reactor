import QtQuick 1.0

Item
{
    width: parent.width; height: parent.height
    id: reactorLed
    property int pwmValue: 0
    property text ledColor: "red"

    function setPWM(value)
    {
        if (value < 0)
        {
            return
        }
        if (value > 255)
        {
            return
        }
        pwmValue = value
        // TODO: redraw
    }
    
    
}
    
