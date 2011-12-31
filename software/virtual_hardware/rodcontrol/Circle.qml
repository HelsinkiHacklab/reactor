//import QtQuick 1.0
import Qt 4.7

Item
{
    id: circle
    property real r: (parent.width<parent.height?parent.width:parent.height)/2
    property color color: "white"

    Rectangle
    {
        width: 2*r
        height: 2*r
        radius: r
        color: circle.color
    }
}
