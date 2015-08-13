import QtQuick 1.0

Rectangle
{
    id: mainContainer
    width: 600; height: 300
    Text
    {
        function setText(value)
        {
            mwtext.text = value
        }
        id: mwtext
        objectName: "mwtext"
        width: parent.width
        anchors.centerIn: parent
        wrapMode: Text.Wrap
        text: "Waiting for data"
        font.pointSize: 48; font.bold: true
    }
}
