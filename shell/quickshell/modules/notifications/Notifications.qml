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

    function resolveSource(value) {
        if (typeof value !== "string" || value.length === 0) return ""
        if (
            value.startsWith("/") ||
            value.startsWith("file:/") ||
            value.startsWith("qrc:/") ||
            value.startsWith("http://") ||
            value.startsWith("https://")
        ) {
            return value
        }
        return Quickshell.iconPath(value, "image-missing")
    }

    function removeNotification(notification) {
        const next = []
        for (const n of root.items) {
            if (n !== notification) next.push(n)
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
                readonly property bool critical: notif && notif.urgency === NotificationUrgency.Critical
                readonly property string imageSource: root.resolveSource(notif ? notif.image : "")
                readonly property string iconName: {
                    if (!notif) return ""
                    if (typeof notif.icon === "string" && notif.icon.length > 0) return notif.icon
                    if (typeof notif.appIcon === "string" && notif.appIcon.length > 0) return notif.appIcon
                    return ""
                }
                readonly property string iconSource: root.resolveSource(iconName)

                Layout.fillWidth: true
                implicitHeight: bodyColumn.implicitHeight + 20
                color: critical ? Theme.Color._errorContainer : Theme.Color._background
                radius: Theme.Style.getMaterialRadius(width, height, "medium")
                border.width: 2
                border.color: Theme.Color._surfaceContainerHigh

                Connections {
                    target: notif
                    function onClosed() {
                        root.removeNotification(notif)
                    }
                }

                Timer {
                    running: notif && !notif.resident
                    interval: notif && notif.expireTimeout > 0 ? notif.expireTimeout : 5000
                    onTriggered: notif.dismiss()
                }

                MouseArea {
                    anchors.fill: parent
                    acceptedButtons: Qt.RightButton
                    onClicked: event => {
                        if (event.button === Qt.RightButton) notif.dismiss()
                    }
                }

                Column {
                    id: bodyColumn
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.margins: 10
                    spacing: 8

                    Row {
                        width: parent.width
                        spacing: 12

                        Rectangle {
                            id: iconBox
                            width: 64
                            height: 64
                            radius: Theme.Style.getMaterialRadius(width, height, "small")
                            color: critical ? Theme.Color._error : Theme.Color._surfaceContainer
                            clip: true

                            Image {
                                id: notifImage
                                anchors.fill: parent
                                source: card.imageSource
                                visible: card.imageSource.length > 0 && status !== Image.Error
                                asynchronous: true
                                cache: false
                            }

                            Image {
                                id: notifIcon
                                anchors.centerIn: parent
                                width: 40
                                height: 40
                                fillMode: Image.PreserveAspectFit
                                source: !notifImage.visible ? card.iconSource : ""
                                visible: !notifImage.visible && card.iconSource.length > 0 && status !== Image.Error
                                asynchronous: true
                            }

                            Text {
                                anchors.centerIn: parent
                                visible: !notifImage.visible && !notifIcon.visible
                                text: critical ? "⚠" : "🔔"
                                color: critical ? Theme.Color._onError : Theme.Color._onSurface
                                font.family: "Iosevka"
                                font.pixelSize: 22
                            }
                        }

                        Column {
                            width: parent.width - iconBox.width - closeWrap.width - 20
                            spacing: 5
                            Layout.alignment: Layout.AlignVCenter  
                            Layout.fillHeight: true

                            Text {
                                width: parent.width
                                text: notif ? (notif.appName || "Notification") : "Notification"
                                color: Theme.Color._onSurfaceVariant
                                font.family: "Iosevka"
                                font.pixelSize: 14
                                elide: Text.ElideRight
                            }

                            Text {
                                width: parent.width
                                text: notif ? (notif.summary || "") : ""
                                color: critical ? Theme.Color._onErrorContainer : Theme.Color._onSurface
                                font.family: "Iosevka"
                                font.pixelSize: 16
                                font.bold: true
                                wrapMode: Text.Wrap
                            }
                        }

                        Rectangle {
                            id: closeWrap
                            width: 28
                            height: 28
                            radius: Theme.Style.getMaterialRadius(width, height, "small")
                            color: Theme.Color._invisible

                            Text {
                                anchors.centerIn: parent
                                text: "✕"
                                color: Theme.Color._onSurface
                                font.family: "Iosevka"
                                font.pixelSize: 14
                            }

                            MouseArea {
                                anchors.fill: parent
                                hoverEnabled: true
                                onClicked: notif.dismiss()
                                onEntered: parent.color = Theme.Color._surfaceContainer
                                onExited: parent.color = Theme.Color._background
                            }
                        }
                    }

                    Text {
                        width: parent.width
                        visible: notif && !!notif.body
                        text: notif ? (notif.body || "") : ""
                        textFormat: Text.RichText
                        color: critical ? Theme.Color._onErrorContainer : Theme.Color._onSurface
                        font.family: "Iosevka"
                        font.pixelSize: 13
                        wrapMode: Text.Wrap
                    }

                    Row {
                        width: parent.width
                        spacing: 6
                        visible: notif && notif.actions && notif.actions.length > 0

                        Repeater {
                            model: notif && notif.actions ? notif.actions : []

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
