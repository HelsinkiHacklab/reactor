//import QtQuick 1.0
import Qt 4.7

Rectangle
{
    id: mainContainer
    width: 768; height: 1024
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
            Grid
            {
                id: gaugeGrid
                width: parent.width; height: parent.height
                columns: 7
                rows: 5
                Repeater
                {
                    model: 32
                    Rectangle
                    {
                        width: gaugeGrid.width/gaugeGrid.columns
                        height: gaugeGrid.height/gaugeGrid.rows
                        color: "transparent"
                        ReactorGauge
                        {
                            objectName: "arduino0_servo" + index
                        }
                    }
                }
            }
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
