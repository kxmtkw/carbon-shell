import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import QtQuick
import QtQuick.Layouts

import "../material" as Material

import "../global" as Global


WrapperRectangle
{
	margin: Material.Style.dpi(70)
	topMargin: Material.Style.dpi(120)

	color: Material.Color.background

	radius: Material.Style.round(Material.Style.roundExtraLargeInc, width, height)

	Process 
	{
		id: power_menu
		running: false
		command: [ "zsh", "-c", "~/.carbon/scripts/power.sh"]
	}

	MouseArea
	{
		Layout.fillHeight: true
		Layout.fillWidth: true

		Text
		{
			id: power_icon
			anchors.centerIn: parent
			
			text: ""

			font.family: "IosevkaTerm Nerd Font"
			font.pixelSize: Material.Style.dpi(260)
			color: Material.Color.on_surface

		}

		onClicked: {
			power_menu.running = true
		}
		
		hoverEnabled: true 

		onEntered: {
			parent.color = Material.Color.surface_container_high
		}

		onExited: {
			parent.color = Material.Color.surface_container
		}

	}
}