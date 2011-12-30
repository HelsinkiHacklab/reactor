import QtQuick 1.0

Item
{
    width: parent.width; height: parent.height
    id: reactorGauge
    
    // Treat these as servos for npw
    property int value: 128
    property int uValue: 1500

    function setPosition(pos)
    {
        value = pos
    }
    function setUSec(value)
    {
        uValue = value
    }
    Rectangle
    {
        id: container
        width: parent.width; height: parent.height
        color: "#dddddd"
        border.color: "black"
        border.width: 2


        // This is actually a circle....
        /*
        Rectangle
        {
            width: parent.width<parent.height?parent.width:parent.height
            height: width
            color: "red"
            border.color: "black"
            border.width: 1
            radius: width*0.5
            Text
            {
                anchors.centerIn: parent
                color: "black"
                text: "Boom"
            }
        }
        */
        Circle
        {
            r: 40
            color: "red"
            Text
            {
                anchors.centerIn: parent
                color: "black"
                text: "Boom"
            }
        }
        
        Text
        {
            id: valueText
            anchors.centerIn: parent
            font.pixelSize: parent.height/3
            text: reactorGauge.value
        }
    }
    
    
}
