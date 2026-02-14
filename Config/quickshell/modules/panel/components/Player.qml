import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import Quickshell.Services.UPower

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import qs.theme as Theme



WrapperRectangle {
	id: player_root

	Layout.fillWidth:       true
	Layout.preferredHeight: Theme.Style.dpi(440)
	Layout.alignment:       Qt.AlignHCenter

	margin: Theme.Style.dpi(70)
	color:  Theme.Color._background
	radius: Theme.Style.round


	Process {
		id: power_menu
		running: false
		command: ["sh", "-c", "~/.carbon/controllers/launch.sh player"]
	}

	MouseArea {
		id: hover_area

		Layout.fillHeight: true
		Layout.fillWidth:  true

		hoverEnabled: true

		Text {
			id:               panelPlayerIcon
			anchors.centerIn: parent
			
			text: " "

			font.family:    Theme.Font.mainFont
			font.pixelSize: Theme.Style.dpi(300)
			color:          Theme.Color._surfaceVariant
		}


		onClicked: {
			power_menu.running = true
		}
		
		onEntered: {
			parent.color = Theme.Color._surfaceContainerLow
		}

		onExited: {
			parent.color = Theme.Color._background
		}

	}


    Process {
        id: icon_updater
        command: ["sh", "-c", "playerctl status"]

        stdout: StdioCollector {
            onStreamFinished: {
                var out = text.trim()
				
                if (out == "Playing") {
                    panelPlayerIcon.color = Theme.Color._primary
                }
                else if (out == "Paused") {
                    panelPlayerIcon.color = Theme.Color._tertiary
                }
                else {
                    panelPlayerIcon.color = Theme.Color._surfaceVariant
                }
            }
        }
    }


    Timer {
        id: update_timer
        interval: 1000
        running: true
        repeat: true
        onTriggered: {
            icon_updater.running = true
        }
    }
}