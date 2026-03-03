import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import Quickshell.Services.UPower

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import qs.theme as Theme



WrapperRectangle 
{
    id: panel_battery

	Layout.fillWidth:       true
	Layout.alignment:       Qt.AlignHCenter
    implicitHeight: 28
    color: Theme.Color._background

	radius: Theme.Style.getMaterialRadius(width, height, "small")

	MouseArea 
    {

        Layout.fillHeight: true
		Layout.fillWidth:  true
        
		hoverEnabled: false

        Text 
        {
            id:               panel_battery_icon
            anchors.centerIn: parent
            
            text: " "

            font.family:    "Iosevka"
            font.pixelSize: 20
            color:          Theme.Color._onSurface
        }


		onClicked: {
			power_menu.running = true
		}
		
		onEntered: {
			parent.color = Theme.Color._background
		}

		onExited: {
			parent.color = Theme.Color._background
		}

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

			panel_battery_icon.text = ""

			if (value >= 98) {
				panel_battery_icon.color = Theme.Color._primary
			}
			else {
				panel_battery_icon.color = Theme.Color._secondary
			}
			
			return
		}

		var sym
		panel_battery_icon.color = Theme.Color._onSurface

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
			panel_battery_icon.color = Theme.Color._error
		}
		else if (value >= 5) {
			sym = "󰁺";
			panel_battery_icon.color = Theme.Color._error
		}
		else {
			sym = "󰂎";
			panel_battery_icon.color = Theme.Color._error
		}

		panel_battery_icon.text = sym
	}

}