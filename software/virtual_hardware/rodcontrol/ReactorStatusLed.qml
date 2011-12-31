//import QtQuick 1.0
import Qt 4.7

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
        color: "black"
        border.color: "black"
        border.width: 2
        Rectangle
        {
            id: light
            anchors.centerIn: parent
            width: (parent.width<parent.height?parent.width:parent.height) * 0.9
            height: width
            color: { var hexPWM = reactorStatusLed.pwmValue.toString(16); return "#" + hexPWM + hexPWM + hexPWM;  }
            radius: width/2
        }
        Rectangle
        {
            id: lid
            width: parent.width; height: parent.height
            color: { if (reactorStatusLed.lidColor == "blue") { return "#600000ff"; } else { return "#60ffffff"; } }
        }

        Text
        {
            anchors.centerIn: parent
            font.pixelSize: parent.height/3
            text: reactorStatusLed.pwmValue
        }
    }
}