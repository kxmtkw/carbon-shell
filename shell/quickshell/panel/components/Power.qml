import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import Quickshell.Services.UPower

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import qs.Config as Theme



WrapperRectangle 
{
    id: panel_power

	Layout.fillWidth:       false
	Layout.preferredWidth:  28
	Layout.preferredHeight: 28
	Layout.alignment:       Qt.AlignVCenter
    implicitHeight: 28
    color: Theme.Color._invisible

	radius: Theme.Style.getMaterialRadius(width, height, "small")

    Process 
    {
        id: panel_power_proc
        command: ["carbon.shell", "controller", "run", "power"]
    }

	MouseArea 
    {
		anchors.fill: parent
        
		hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        Text 
        {
            id:               panel_power_icon
            anchors.centerIn: parent
            
            text: ""

            font.family:    Theme.Style.font
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
			parent.color = Theme.Color._invisible
		}

	}
}
