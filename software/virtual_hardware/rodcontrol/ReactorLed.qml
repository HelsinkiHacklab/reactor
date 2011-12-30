import QtQuick 1.0

Item
{
    width: parent.width; height: parent.height
    id: reactorLed
    property int pwmValue: 0
    property string ledColor: "red"

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
    Rectangle
    {
        id: container
        width: parent.width; height: parent.height
        color: "#dddddd"
        border.color: "black"
        border.width: 2
        Text
        {
            anchors.centerIn: parent
            font.pixelSize: parent.height/3
            text: reactorLed.pwmValue
        }
    }
    
    
}
