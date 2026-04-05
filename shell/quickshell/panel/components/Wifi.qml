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
    id: panel_wifi

	Layout.fillWidth:       false
	Layout.preferredWidth:  28
	Layout.preferredHeight: 28
	Layout.alignment:       Qt.AlignVCenter
    implicitHeight: 28
    color: Theme.Color._invisible

	radius: Theme.Style.getMaterialRadius(width, height, "small")


    Process
    {
        id: panel_wifi_process
        running: false
        command: ["sh", "-c", "carbon.shell controller run networker"]
    }

	MouseArea 
    {
		anchors.fill: parent
        
		hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        Text 
        {
            id:               panel_wifi_icon
            anchors.centerIn: parent
            
            text: " "

            font.family:    Theme.Style.font
            font.pixelSize: 19
            color:          Theme.Color._onSurface
        }


		onClicked: {
			panel_wifi_process.running = true
		}
		
		onEntered: {
			parent.color = Theme.Color._surfaceContainer
		}

		onExited: {
			parent.color = Theme.Color._invisible
		}

	}

}
