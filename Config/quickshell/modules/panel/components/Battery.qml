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
	Layout.fillWidth:       true
	Layout.preferredHeight: Theme.Style.dpi(440)
	Layout.alignment:       Qt.AlignHCenter

	margin: Theme.Style.dpi(70)
	color:  Theme.Color._background
	radius: Theme.Style.round


	Process {
		id: power_menu
		running: false
		command: ["sh", "-c", "~/.carbon/controllers/launch.sh battery"]
	}

	MouseArea {
		Layout.fillHeight: true
		Layout.fillWidth:  true

		hoverEnabled: true

		Text {
			id:               panelBatteryIcon
			anchors.centerIn: parent
			
			text: " "

			font.family:    Theme.Font.mainFont
			font.pixelSize: Theme.Style.dpi(300)
			color:          Theme.Color._onSurface
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


		Timer {
			id: update_timer
			interval: 250
			running: true
			repeat: true
			onTriggered: {
				parent.setSymbol()
			}
		}

		function setSymbol() {
			var value = UPower.displayDevice.percentage * 100;

			if (!UPower.onBattery) {

				panelBatteryIcon.text = ""
				panelBatteryIcon.font.pixelSize = Theme.Style.dpi(300)

				if (value >= 98) {
					panelBatteryIcon.color = Theme.Color._primary
				}
				else {
					panelBatteryIcon.color = Theme.Color._secondary
				}
				
				return
			}

			var sym
			panelBatteryIcon.color = Theme.Color._onSurface

			if (value >= 95) {
				sym = "󰁹";
			} 
			else if (value >= 85) {
				sym = "󰂂";
			}
			else if (value >= 75) {
				sym = "󰂁";
			}
			else if (value >= 65) {
				sym = "󰂀";
			}
			else if (value >= 55) {
				sym = "󰁿";
			}
			else if (value >= 45) {
				sym = "󰁾";
			}
			else if (value >= 35) {
				sym = "󰁽";
			}
			else if (value >= 25) {
				sym = "󰁼";
			}
			else if (value >= 15) {
				sym = "󰁻";
				panelBatteryIcon.color = Theme.Color._error
			}
			else if (value >= 5) {
				sym = "󰁺";
				panelBatteryIcon.color = Theme.Color._error
			}
			else {
				sym = "󰂎";
				panelBatteryIcon.color = Theme.Color._error
			}

			panelBatteryIcon.text = sym
		}

	}
}