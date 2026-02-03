import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import Quickshell.Services.UPower

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import "../material" as Material

import "../global" as Global


WrapperRectangle
{
	margin: Material.Style.dpi(70)
	topMargin: Material.Style.dpi(120)

	color: Material.Color._background

	radius: Material.Style.round(Material.Style.roundExtraLargeInc, width, height)

	Process 
	{
		id: power_menu
		running: false
		command: ["sh", "-c", "~/.carbon/controllers/launch.sh battery"]
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
			font.pixelSize: Material.Style.dpi(260)
			color: Material.Color._onSurface

		}


		onClicked: {
			power_menu.running = true
		}
		
		hoverEnabled: true 

		onEntered: {
			parent.color = Material.Color._surfaceContainer
		}

		onExited: {
			parent.color = Material.Color._background
		}


		function setSymbol()
		{
			var value = UPower.displayDevice.percentage * 100;

			if (!UPower.onBattery)
			{
				battery_icon.text = ""
				battery_icon.font.pixelSize = Material.Style.dpi(260)

				if (value >= 98)
				{
					battery_icon.color = Material.Color._primary
				}
				else
				{
					battery_icon.color = Material.Color._secondary
				}
				
				return
			}

			var sym
			battery_icon.color = Material.Color._onSurface

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
				battery_icon.color = Material.Color._error
			}
			else if (value >= 5)
			{
				sym = "󰁺";
				battery_icon.color = Material.Color._error
			}
			else
			{
				sym = "󰂎";
				battery_icon.color = Material.Color._error
			}

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