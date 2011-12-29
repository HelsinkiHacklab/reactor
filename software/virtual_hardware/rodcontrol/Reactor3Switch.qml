import QtQuick 1.0

Item
{
    id: reactor3Switch
    
    property int value: 0
    
    Rectangle
    {
        width: 60
        Row
        {
            Rectangle
            {
                width: 30; height: 30
                color: "red"
                Text
                {
                    text: reactor3Switch.value
                }
            }
            Rectangle
            {
                width: 30; height: 30
                Column
                {
                    Rectangle
                    {
                        width: 15; height: 15
                        color: "green"
                        Text
                        {
                            text: "-"
                        }
                        MouseArea
                        {
                            anchors.fill: parent
                            id: click_down
                            onClicked: { reactor3Switch.value = reactor3Switch.value-1 }
                        }
                    }
                    Rectangle
                    {
                        width: 15; height: 15
                        Text
                        {
                            text: "+"
                        }
                        MouseArea
                        {
                            anchors.fill: parent
                            id: click_up
                            onClicked: { reactor3Switch.value = reactor3Switch.value+1 }
                        }
                    }
                }
            }
        }
    }
}