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
                            objectName: "servo" + index
                        }
                    }
                }
            }
        }
        Rectangle
        {
            width: parent.width; height: parent.height/3
            RodSwitches{}
        }
    }
}
