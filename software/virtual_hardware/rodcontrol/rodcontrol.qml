import QtQuick 1.0

Rectangle
{
    id: switches
    width: 400; height: 400;
    // Rows
    Column
    {
        // Row 1
        Rectangle
        {
            width: switches.width; height: 30
            Row
            {
                spacing: 0
                Rectangle
                {
                    width: 30; height: 30
                    Reactor3Switch
                    {
                        upPin: 1
                        downPin: 2
                    }
                }
                Rectangle
                {
                    width: 30; height: 30
                    color: "black"
                }
                Rectangle
                {
                    width: 30; height: 30
                    color: "black"
                }
                Rectangle
                {
                    width: 30; height: 30
                    Text
                    {
                        text: "1"
                        font.pointSize: 15
                    }
                }
                Rectangle
                {
                    width: 30; height: 30
                    Text
                    {
                        text: "2"
                        font.pointSize: 15
                    }
                }
                Rectangle
                {
                    width: 30; height: 30
                    Text
                    {
                        text: "3"
                        font.pointSize: 15
                    }
                }
                Rectangle
                {
                    width: 30; height: 30
                    color: "black"
                }
                Rectangle
                {
                    width: 30; height: 30
                    color: "black"
                }
            }
        }
        spacing: 0
        /*
        Repeater 
        {
            id: rowrepeater
            model: 7
            Rectangle
            {
                width: switches.width; height: 30
                Row
                {
                    spacing: 0
                    Repeater 
                    {
                        model: 7
                        id: columnrepeater
                        Rectangle
                        {
                            width: 30; height: 30
                            Text
                            {
                                text: index
                                font.pointSize: 15
                            }
                        }
                    }
                }
            }
        }
        */
    }
    

    /*
    Grid
    {
        x: 5; y: 5
        rows: 5; columns: 5; spacing: 10
        Repeater 
        {
            model: 24
            Rectangle
            {
                width: 70; height: 70
                color: "lightgreen"
                Text
                {
                    text: index
                    font.pointSize: 30
                    anchors.centerIn: parent
                }
            }
        }
    }
    */

}