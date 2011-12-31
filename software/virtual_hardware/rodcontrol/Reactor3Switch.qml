//import QtQuick 1.0
import Qt 4.7

Item
{
    width: parent.width; height: parent.height
    id: reactor3Switch
    
    property int upPin: 0
    property int downPin: 0
    property int value: 0
    property int prevValue: 0
    property string boardName: "arduino1"

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
        Row
        {
            width: parent.width; height: parent.height
            Rectangle
            {
                width: parent.width/2; height: parent.height
                color: "transparent"
                Text
                {
                    anchors.centerIn: parent
                    font.pixelSize: parent.height/3
                    text: reactor3Switch.value
                }
            }
            Rectangle
            {
                width: parent.width/2; height: parent.height
                color: "transparent"
                Column
                {
                    width: parent.width; height: parent.height
                    Rectangle
                    {
                        width: parent.width; height: parent.height/2
                        color: "transparent"
                        Text
                        {
                            anchors.centerIn: parent
                            font.pixelSize: parent.height
                            text: "+"
                        }
                        MouseArea
                        {
                            anchors.fill: parent
                            id: click_up
                            onClicked: { reactor3Switch.up() }
                        }
                    }
                    Rectangle
                    {
                        width: parent.width; height: parent.height/2
                        color: "transparent"
                        Text
                        {
                            anchors.centerIn: parent
                            text: "-"
                            font.pixelSize: parent.height
                        }
                        MouseArea
                        {
                            anchors.fill: parent
                            id: click_down
                            onClicked: { reactor3Switch.down() }
                        }
                    }
                }
            }
        }
    }
}