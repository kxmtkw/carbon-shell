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
		command: ["sh", "-c", "carbon.controller player"]
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


			ColorAnimation on color {
				id: music_playing_animation
				from: panelPlayerIcon.color
				to: Theme.Color._primary
				duration: 500 
			}

			ColorAnimation on color {
				id: music_paused_animation
				from: panelPlayerIcon.color
				to: Theme.Color._tertiary
				duration: 500
			}

			ColorAnimation on color {
				id: music_stopped_animation
				from: panelPlayerIcon.color
				to: Theme.Color._surfaceVariant
				duration: 500 
			}

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
                    music_playing_animation.running = true
                }
                else if (out == "Paused") {
                    music_paused_animation.running = true
                }
                else {
                    music_stopped_animation.running = true
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