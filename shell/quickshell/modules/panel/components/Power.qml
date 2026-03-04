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
    id: panel_power

	Layout.fillWidth:       true
	Layout.alignment:       Qt.AlignHCenter
    implicitHeight: 28
    color: true ? Theme.Color._invisible : Theme.Color._invisible

	radius: Theme.Style.getMaterialRadius(width, height, "small")

    Process 
    {
        id: panel_power_proc
        command: ["sh", "-c", "carbon.controller power"]
    }

	MouseArea 
    {

        Layout.fillHeight: true
		Layout.fillWidth:  true
        
		hoverEnabled: true

        Text 
        {
            id:               panel_power_icon
            anchors.centerIn: parent
            
            text: ""

            font.family:    "Iosevka"
            font.pixelSize: 20
            color:          Theme.Color._onSurface
        }


		onClicked: {
			panel_power_proc.running = true
		}
		
		onEntered: {
			parent.color = Theme.Color._surfaceContainer
		}

		onExited: {
			parent.color = Theme.Color._background
		}

	}
}