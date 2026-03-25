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
    id: panel_launcher

	Layout.fillWidth:       false
	Layout.preferredWidth:  30
	Layout.preferredHeight: 30
	Layout.alignment:       Qt.AlignVCenter
    color: Theme.Color._invisible

	radius: Theme.Style.getMaterialRadius(width, height, "small")


    Process
    {
        id: panel_launcher_process
        running: false
        command: ["sh", "-c", "carbon.controller launcher"]
    }

	MouseArea 
    {
		anchors.fill: parent
        
		hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        Text 
        {
            id:               panel_launcher_icon
            anchors.centerIn: parent
            
            text: "󰌽"

            font.family:    Theme.Style.font
            font.pixelSize: 22
            color:          Theme.Color._onSurface
        }


		onClicked: {
			panel_launcher_process.running = true
		}
		
		onEntered: {
			parent.color = Theme.Color._surfaceContainer
		}

		onExited: {
			parent.color = Theme.Color._invisible
		}

	}

}
