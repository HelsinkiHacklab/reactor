import QtQuick 1.0
import "../ReactorLib"

Rectangle
{
    id: mainContainer
    width: 600; height: 900
    Column
    {
        width: parent.width; height: parent.height
        Rectangle
        {
            width: parent.width; height: parent.height/4
            color: "transparent"
            LidLights{}
        }
        Rectangle
        {
            width: parent.width; height: parent.height/4*2
            color: "transparent"
            RodGauges{}
        }
        Rectangle
        {
            width: parent.width; height: parent.height/4
            color: "transparent"
            Row
            {
                width: parent.width; height: parent.height
                Rectangle
                {
                    width: parent.width/5*4;
                    height: parent.height
                    RodSwitches{}
                }
                Rectangle
                {
                    width: parent.width/5;
                    height: parent.height
                    color: "lightgreen"
                    Text
                    {
                        width: parent.width
                        anchors.centerIn: parent
                        wrapMode: Text.Wrap
                        text: "TODO: Add the remaining switches (currently unwired in real HW)"
                    }
                }
            }
        }
    }
}
