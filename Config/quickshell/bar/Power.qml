import Quickshell
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

	color: Material.Color.surface_container

	radius: Material.Style.round(Material.Style.roundExtraLargeInc, width, height)


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
			Global.State.powerMenuShown = !Global.State.powerMenuShown
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