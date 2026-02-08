import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import Quickshell.Services.UPower

import QtQuick
import QtQuick.Layouts

import qs.theme as Theme



WrapperRectangle {
	Layout.fillWidth:       true
	Layout.preferredHeight: Theme.Style.dpi(400)
	Layout.alignment:       Qt.AlignHCenter | Qt.AlignBottom

	color:  Theme.Color._background
	radius: Theme.Style.round

	Process {
		id:      power_menu
		running: false
		command: ["sh", "-c", "~/.carbon/controllers/launch.sh launcher_apps"]
	}

	MouseArea {
		Layout.fillHeight: true
		Layout.fillWidth:  true
	
		hoverEnabled: true 

		Text {
			id: panelArchIcon
			anchors.centerIn: parent
			
			text: "󰣇"

			font.family:    Theme.Font.mainFont
			font.pixelSize: Theme.Style.dpi(320)
			color:          Theme.Color._onSurface

		}


		onClicked: {
			power_menu.running = true
		}
		
		onEntered: {
			parent.color = Theme.Color._surfaceContainer
		}

		onExited: {
			parent.color = Theme.Color._background
		}

		
	}
}