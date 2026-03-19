import Quickshell
import Quickshell.Widgets
import Quickshell.Services.Notifications
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import qs.theme as Theme

WrapperRectangle {
    id: card

    property var notifData
    property bool notifIsCritical: notifData.urgency === NotificationUrgency.Critical

    signal closed()

    Layout.fillWidth: true
    implicitHeight: content.implicitHeight + 28
    implicitWidth: 600
    color: notifIsCritical ? Theme.Color._primaryContainer : Theme.Color._background
    radius: Theme.Style.getMaterialRadius(width, height, "large")
    opacity: 100

    Column {
        id: content

        anchors {
            top: parent.top
            left: parent.left
            right: parent.right            
            bottom: parent.bottom
            margins: 20
        }

        spacing: 10

        RowLayout {
            width: parent.width
            spacing: 6

            IconImage {
                visible: false
                source: "notifData.image://icon/" + card.notifData.appIcon
                height: 22
                width: 22
                Layout.alignment: Qt.AlignVCenter
                smooth: true
            }

            Text {
                text: card.notifData.appName
                font.pixelSize: 14
                font.italic: true
                color: card.notifIsCritical ? Theme.Color._onPrimaryContainer : Theme.Color._onSurface
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignVCenter
            }

            Item {
                width: 18
                height: 18
                Layout.alignment: Qt.AlignVCenter

                Text {
                    anchors.centerIn: parent
                    text: ""
                    font.pixelSize: 16
                    color: card.notifIsCritical ? Theme.Color._onPrimaryContainer : Theme.Color._onSurface
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        card.opacity = 0
                        card.closed()
                    }
                }
            }
        }

        RowLayout {
            width: parent.width
            spacing: 20

            Image {
                source: card.notifData.image
                visible: card.notifData.image !== ""
                Layout.preferredWidth: 140
                Layout.preferredHeight: 140
                fillMode: Image.PreserveAspectFit
                smooth: true
            }

            ColumnLayout {
                Layout.fillWidth: true
                spacing: 5

                Text {
                    text: card.notifData.summary
                    font.pixelSize: 22
                    font.weight: Font.Medium
                    color: card.notifIsCritical ? Theme.Color._onPrimaryContainer : Theme.Color._onSurface
                    Layout.fillWidth: true
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                    maximumLineCount: 1
                }

                Text {
                    text: card.notifData.body
                    font.pixelSize: 14
                    color: card.notifIsCritical ? Theme.Color._onPrimaryContainer : Theme.Color._onSurface
                    Layout.fillWidth: true
                    wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                    visible: card.notifData.body !== ""
                }
            }
        }
    }
}