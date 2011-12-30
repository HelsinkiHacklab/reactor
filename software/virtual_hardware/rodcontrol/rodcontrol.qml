import QtQuick 1.0

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
            color: "lightgreen"
            LidLights{}
        }
        Rectangle
        {
            width: parent.width; height: parent.height/4*2
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
            width: parent.width; height: parent.height/4
            RodSwitches{}
        }
    }
}
