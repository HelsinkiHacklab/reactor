import QtQuick 1.0
import "../ReactorLib"

Rectangle
{
    id: mainContainer
    width: 600; height: 400
    Column
    {
        width: parent.width; height: parent.height
        Rectangle
        {
            width: parent.width; height: parent.height/4*3
            color: "transparent"
            LidRodCovers{}
        }
        Rectangle
        {
            width: parent.width; height: parent.height/4
            color: "transparent"
            Text
            {
                text: "TODO: Smoke machine state indicator"
            }
        }
    }
}
