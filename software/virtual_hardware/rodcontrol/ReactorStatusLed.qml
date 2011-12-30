import QtQuick 1.0

Item
{
    width: parent.width; height: parent.height
    id: reactorStatusLed
    property int pwmValue: 0
    
    property string lidColor: "white" // The other alternative is "blue"
    property string label: ""

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
        color: "#eeeeee"
        border.color: "black"
        border.width: 2
        Text
        {
            anchors.centerIn: parent
            font.pixelSize: parent.height/3
            text: reactorStatusLed.pwmValue
        }
    }
}