import Quickshell
import Quickshell.Widgets
import Quickshell.Services.Notifications
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import qs.theme as Theme

PanelWindow {
    id: root

    anchors {
        top: true
        right: true
    }

    margins {
        top: 16
        right: 16
    }

    color: "transparent"
    implicitWidth: 420
    implicitHeight: notifColumn.implicitHeight

    property var items: []

    function removeNotification(notification) {
        const next = []
        for (const n of root.items) {
            if (n !== notification) {
                next.push(n)
            }
        }
        root.items = next
    }

    NotificationServer {
        id: notifServer

        keepOnReload: false
        actionsSupported: true
        bodyHyperlinksSupported: true
        bodyImagesSupported: true
        bodyMarkupSupported: true
        imageSupported: true
        persistenceSupported: true

        onNotification: notification => {
            notification.tracked = true
            const next = root.items.slice()
            next.unshift(notification)
            root.items = next
        }
    }

    ColumnLayout {
        id: notifColumn
        width: parent.width
        spacing: 10

        Repeater {
            model: root.items

            Rectangle {
                id: card

                required property var modelData
                readonly property var notif: modelData
                readonly property bool hasImage: !!notif.image
                readonly property bool hasAppIcon: !!notif.appIcon
                readonly property bool critical: notif.urgency === NotificationUrgency.Critical

                radius: Theme.Style.getMaterialRadius(width, height, "medium")
                color: critical ? Theme.Color._errorContainer : Theme.Color._surfaceContainer
                border.width: 1
                border.color: Theme.Color._outlineVariant
                Layout.fillWidth: true
                implicitHeight: content.implicitHeight + 20

                Connections {
                    target: notif
                    function onClosed() {
                        root.removeNotification(notif)
                    }
                }

                Timer {
                    id: expireTimer
                    running: !notif.resident
                    interval: notif.expireTimeout > 0 ? notif.expireTimeout : 5000
                    onTriggered: notif.dismiss()
                }

                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.LeftButton | Qt.RightButton
                    hoverEnabled: true
                    onClicked: event => {
                        if (event.button === Qt.RightButton) {
                            notif.dismiss()
                        }
                    }
                }

                ColumnLayout {
                    id: content
                    anchors.fill: parent
                    anchors.margins: 10
                    spacing: 8

                    RowLayout {
                        spacing: 10
                        Layout.fillWidth: true

                        Item {
                            id: iconSlot
                            implicitWidth: 36
                            implicitHeight: 36

                            Image {
                                anchors.fill: parent
                                fillMode: Image.PreserveAspectFit
                                visible: card.hasImage
                                source: card.hasImage ? notif.image : ""
                                asynchronous: true
                                cache: false
                            }

                            Image {
                                anchors.fill: parent
                                fillMode: Image.PreserveAspectFit
                                visible: !card.hasImage && card.hasAppIcon
                                source: !card.hasImage && card.hasAppIcon ? Quickshell.iconPath(notif.appIcon) : ""
                                asynchronous: true
                            }

                            Text {
                                anchors.centerIn: parent
                                visible: !card.hasImage && !card.hasAppIcon
                                text: ""
                                font.family: "Iosevka"
                                font.pixelSize: 20
                                color: Theme.Color._onSurface
                            }
                        }

                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 2

                            Text {
                                Layout.fillWidth: true
                                text: notif.appName || "Notification"
                                color: Theme.Color._onSurfaceVariant
                                font.family: "Iosevka"
                                font.pixelSize: 12
                                elide: Text.ElideRight
                            }

                            Text {
                                Layout.fillWidth: true
                                text: notif.summary || ""
                                color: Theme.Color._onSurface
                                font.family: "Iosevka"
                                font.pixelSize: 14
                                font.bold: true
                                wrapMode: Text.Wrap
                            }
                        }

                        Button {
                            text: "×"
                            onClicked: notif.dismiss()
                        }
                    }

                    Text {
                        Layout.fillWidth: true
                        visible: !!notif.body
                        text: notif.body || ""
                        textFormat: Text.RichText
                        color: Theme.Color._onSurface
                        font.family: "Iosevka"
                        font.pixelSize: 13
                        wrapMode: Text.Wrap
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 6
                        visible: notif.actions && notif.actions.length > 0

                        Repeater {
                            model: notif.actions || []

                            Button {
                                required property var modelData
                                text: modelData.text
                                onClicked: modelData.invoke()
                            }
                        }
                    }
                }
            }
        }
    }
}
