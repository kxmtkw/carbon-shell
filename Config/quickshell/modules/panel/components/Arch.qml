import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import Quickshell.Services.UPower

import QtQuick
import QtQuick.Layouts

import qs.theme as Theme



WrapperRectangle
{
	margin: Theme.Style.dpi(70)
	topMargin: Theme.Style.dpi(120)
	bottomMargin: Theme.Style.dpi(120)

	color: Theme.Color._background

	radius: Theme.Style.round

	Process 
	{
		id: power_menu
		running: false
		command: ["sh", "-c", "~/.carbon/controllers/launch.sh launcher_apps"]
	}

	MouseArea
	{
		Layout.fillHeight: true
		Layout.fillWidth: true

		Text
		{
			id: battery_icon
			anchors.centerIn: parent
			
			text: "󰣇"

			font.family: "IosevkaTerm Nerd Font"
			font.pixelSize: Theme.Style.dpi(320)
			color: Theme.Color._onSurface

		}


		onClicked: {
			power_menu.running = true
		}
		
		hoverEnabled: true 

		onEntered: {
			parent.color = Theme.Color._surfaceContainer
		}

		onExited: {
			parent.color = Theme.Color._background
		}
	}
}