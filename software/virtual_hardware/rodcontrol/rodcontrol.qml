import QtQuick 1.0

Rectangle
{
    id: mainContainer
    width: 300; height: 800
    Column
    {
        width: parent.width; height: parent.height
        Rectangle
        {
            width: parent.width; height: parent.height/3
            color: "lightgreen"
            Text
            {
                anchors.centerIn: parent
                text: "status lights panel placeholder"
            }
        }
        Rectangle
        {
            width: parent.width; height: parent.height/3
            color: "red"
            Text
            {
                anchors.centerIn: parent
                text: "gauges panel placeholder"
            }
        }
        Rectangle
        {
            width: parent.width; height: parent.height/3
            RodSwitches{}
        }
    }
}
