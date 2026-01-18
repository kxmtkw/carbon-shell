import Quickshell
import Quickshell.Widgets
import Quickshell.Hyprland
import QtQuick
import QtQuick.Layouts

import "../material" as Material

import "../global" as Global

WrapperRectangle {
    margin: Material.Style.dpi(400)
    color: Material.Color.background
    width: parent.width
    height: parent.height
    radius: Material.Style.round(Material.Style.roundMedium, width, height)

    ColumnLayout {
        anchors.centerIn: parent
        spacing: Material.Style.dpi(10)
        width: parent.width
        height: parent.height

        Repeater {
            model: [
                "  Shutdown",
                "  Reboot",
                "  Lock",
                "  Sleep",
                "  Hibernate",
                "  BIOS"
            ]

            delegate: Rectangle {
                id: rect
                anchors.horizontalCenter: parent.horizontalCenter   
                Layout.fillWidth: true
                Layout.preferredHeight: Material.Style.dpi(600)
                color: Material.Color.background
                radius: Material.Style.round(Material.Style.roundLarge, width, height)

                Text {
                    anchors.verticalCenter: parent.verticalCenter   
                    anchors.left: parent.left                        
                    anchors.leftMargin: Material.Style.dpi(200)

                    color: Material.Color.on_surface
                    text: modelData
                    font.family: "Iosevka Nerd Font"
                    font.pointSize: Material.Style.dpi(180)
                }


                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true

                    onEntered: rect.color = Material.Color.surface_container
                    onExited: rect.color = Material.Color.background
                    onClicked: Global.State.powerMenuShown = false
                }
            }
        }
    }
}
