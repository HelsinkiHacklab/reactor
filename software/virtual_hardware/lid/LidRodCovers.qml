import QtQuick 1.0
import "../ReactorLib"

Rectangle
{
    id: lidLights
    width: parent.width; height: parent.height
    // Rows
    Column
    {
        width: parent.width; height: parent.height
        // Row 1
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 0
                        downPin: 0
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 1
                        downPin: 1
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 2
                        downPin: 2
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
            }
        }

        // Row 2
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 3
                        downPin: 3
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    // TODO: one of those special nonclickable covers
                    Text
                    {
                        text: "TODO"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 5
                        downPin: 5
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 6
                        downPin: 6
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 7
                        downPin: 7
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
            }
        }

        // Row 3
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 8
                        downPin: 8
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 9
                        downPin: 9
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 10
                        downPin: 10
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 11
                        downPin: 11
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 12
                        downPin: 12
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    // TODO: one of those special nonclickable covers
                    Text
                    {
                        text: "TODO"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 14
                        downPin: 14
                    }
                }
            }
        }

        // Row 4
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 15
                        downPin: 15
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 16
                        downPin: 16
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 17
                        downPin: 17
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 18
                        downPin: 18
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 19
                        downPin: 19
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 20
                        downPin: 20
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 21
                        downPin: 21
                    }
                }
            }
        }

        // Row 5
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 22
                        downPin: 22
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    // TODO: one of those special nonclickable covers
                    Text
                    {
                        text: "TODO"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 24
                        downPin: 24
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 25
                        downPin: 25
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 26
                        downPin: 26
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 27
                        downPin: 27
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 28
                        downPin: 28
                    }
                }
            }
        }

        // Row 6
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 29
                        downPin: 29
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 30
                        downPin: 30
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 31
                        downPin: 31
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    // TODO: one of those special nonclickable covers
                    Text
                    {
                        text: "TODO"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 33
                        downPin: 33
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
            }
        }

        // Row 7
        Rectangle
        {
            width: parent.width; height: parent.height/7
            Row
            {
                width: parent.width; height: parent.height
                spacing: 0
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 34
                        downPin: 34
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 35
                        downPin: 35
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorRodCover
                    {
                        ledNo: 36
                        downPin: 36
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    color: "black"
                }
            }
        }
    // End column
    }
}