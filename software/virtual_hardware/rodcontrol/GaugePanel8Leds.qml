import QtQuick 1.0

Item
{
    width: parent.width; height: parent.height
    id: gaugePanel8Leds

    property string boardName: "arduino1"
    property int index_base: 0
    Grid
    {
        width: parent.width; height: parent.height
        id: ledGrid
        columns: 2
        rows: 4
        Repeater
        {
            id: ledRepeater
            model: 8
            Rectangle
            {
                width: ledGrid.width/2; height: ledGrid.height/4
                ReactorLed
                {
                    ledColor: { if ( (ledRepeater.index % 2) == 1) { return "green"; } else { return "red"; } }
                    objectName: gaugePanel8Leds.boardName + "_led" + (gaugePanel8Leds.index_base + ledRepeater.index)
                }
            }
        }
    }
}