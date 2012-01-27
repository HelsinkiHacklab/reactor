import QtQuick 1.0

Item
{
    width: parent.width; height: parent.height
    id: reactorRodCover
    
    property int downPin: 0
    property int ledValue: 0
    property int ledNo: 0
    property int value: 0
    property int prevValue: 0
    property string boardName: "arduino2"
    property string namePrefix: "arduino2_pca9635RGBJBOL0_led"

    function up()
    {
        if (value < 1)
        {
            value = value+1;
            controller.switch_changed(this);
            prevValue = value;
        }
    }
    function down()
    {
        if (value > -1)
        {
            value = value-1;
            controller.switch_changed(this);
            prevValue = value;
        }
    }
    
    Rectangle
    {
        id: container
        width: parent.width; height: parent.height
        color: "#c0c0c0"
        border.color: "black"
        border.width: 2
        ReactorLed
        {
            objectName: reactorRodCover.namePrefix + reactorRodCover.ledNo
        }
        MouseArea
        {
            anchors.fill: parent
            id: click_down
            onPressed: { reactorRodCover.down() }
            onReleased: { reactorRodCover.up() }
        }
    }
}