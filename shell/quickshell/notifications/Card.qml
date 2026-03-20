import Quickshell
import Quickshell.Widgets
import Quickshell.Services.Notifications
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import qs.Config as Theme

WrapperRectangle {
    id: card

    property var notifData
    property bool notifIsCritical: notifData.urgency === NotificationUrgency.Critical


    Layout.fillWidth: true
    implicitHeight: content.implicitHeight + 42
    implicitWidth: 600
    color: notifIsCritical ? Theme.Color._primaryContainer : Theme.Color._background
    radius: Theme.Style.getMaterialRadius(width, height, "large")
    border.width: 2
    border.color: Theme.Color._invisible




    signal closed()

    function remove() {
        close_timer.running = true
        card.color = "transparent"
        card.opacity = 0
        card.implicitHeight = 0
        card.color = Theme.Color._invisible
    }

    Timer {
        id: close_timer
        interval: 500
        running: false
        onTriggered: {card.closed()}
    }

    Behavior on implicitHeight {
        NumberAnimation {
            duration: 50
            easing.type: Easing.InOutQuad
        }
    }

    Behavior on opacity {
        NumberAnimation {
            duration: 100
            easing.type: Easing.InOutQuad
        }
    }

    Column {
        id: content

        anchors {
            top: parent.top
            left: parent.left
            right: parent.right            
            bottom: parent.bottom
            margins: 20
        }

        spacing: 5

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
                        card.remove()
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