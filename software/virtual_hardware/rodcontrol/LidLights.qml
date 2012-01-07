import QtQuick 1.0

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
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led0"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led1"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led2"
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
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led3"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led4"
                        lidColor: "blue"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led5"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led6"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led7"
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
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led8"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led9"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led10"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led11"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led12"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led13"
                        lidColor: "blue"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led14"
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
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led15"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led16"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led17"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led18"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led19"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led20"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led21"
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
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led22"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led23"
                        lidColor: "blue"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led24"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led25"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led26"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led27"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led28"
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
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led29"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led30"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led31"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led32"
                        lidColor: "blue"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led33"
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
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led34"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led35"
                    }
                }
                Rectangle
                {
                    width: parent.width/7; height: parent.height
                    ReactorStatusLed
                    {
                        objectName: "arduino0_pca9635RGBJBOL0_led36"
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