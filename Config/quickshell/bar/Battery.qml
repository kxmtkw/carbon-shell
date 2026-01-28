import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import Quickshell.Services.UPower

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
		command: [ "~/.carbon/controllers/launch.sh", "battery"]
	}

	MouseArea
	{
		Layout.fillHeight: true
		Layout.fillWidth: true

		Text
		{
			id: battery_icon
			anchors.centerIn: parent
			
			text: ""

			font.family: "IosevkaTerm Nerd Font"
			font.pixelSize: Material.Style.dpi(280)
			color: Material.Color.on_surface

		}


		onClicked: {
			power_menu.running = true
		}
		
		hoverEnabled: true 

		onEntered: {
			parent.color = Material.Color.surface_container
		}

		onExited: {
			parent.color = Material.Color.background
		}


		function setSymbol()
		{
			
			if (!UPower.onBattery)
			{
				battery_icon.text = ""
				battery_icon.font.pixelSize = Material.Style.dpi(260)
				battery_icon.color = Material.Color.primary
				return
			}

			var value = UPower.displayDevice.percentage * 100;
			var sym

			if (value >= 95)
			{
				sym = "󰁹";
			}
			else if (value >= 85)
			{
				sym = "󰂂";
			}
			else if (value >= 75)
			{
				sym = "󰂁";
			}
			else if (value >= 65)
			{
				sym = "󰂀";
			}
			else if (value >= 55)
			{
				sym = "󰁿";
			}
			else if (value >= 45)
			{
				sym = "󰁾";
			}
			else if (value >= 35)
			{
				sym = "󰁽";
			}
			else if (value >= 25)
			{
				sym = "󰁼";
			}
			else if (value >= 15)
			{
				sym = "󰁻";
			}
			else if (value >= 5)
			{
				sym = "󰁺";
			}
			else
			{
				battery_icon.text = "󰂎";
				battery_icon.color = Material.Color.error
			}

			battery_icon.color = Material.Color.on_surface
			battery_icon.text = sym
		}


		Timer
		{
			id: update_timer
			interval: 250
			running: true
			repeat: true
			onTriggered: {
				parent.setSymbol()
			}
		}


	}
}