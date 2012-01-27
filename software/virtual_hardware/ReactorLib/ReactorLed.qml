import QtQuick 1.0

Item
{
    width: parent.width; height: parent.height
    id: reactorLed
    property int pwmValue: 0
    // Supported colors: "red","green" TODO: add "white".
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
    }
    Rectangle
    {
        id: container
        color: "transparent"
        width: parent.width; height: parent.height
        Rectangle
        {
            id: light
            anchors.centerIn: parent
            width: (parent.width<parent.height?parent.width:parent.height) * 0.9
            height: width
            color: { var hexPWM = reactorLed.pwmValue.toString(16); return "#" + hexPWM + hexPWM + hexPWM;  }
            radius: width/2
        }
        Rectangle
        {
            id: lid
            anchors.centerIn: parent
            width: (parent.width<parent.height?parent.width:parent.height) * 0.9
            height: width
            border.color: "black"
            border.width: 2
            color: { if (reactorLed.ledColor == "green") { return "#6000FF00"; } else { return "#60FF0000"; } }
            radius: width/2
        }
        
        
        Text
        {
            anchors.centerIn: parent
            font.pixelSize: parent.height/3
            text: reactorLed.pwmValue
        }
    }
    
    
}
