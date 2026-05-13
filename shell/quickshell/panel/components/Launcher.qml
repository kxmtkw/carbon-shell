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
        command: ["carbon.shell", "controller", "run", "launcher"]
    }

	MouseArea 
    {
		anchors.fill: parent
        
		hoverEnabled: true
        cursorShape: Qt.PointingHandCursor


		onClicked: {
			panel_launcher_process.running = true
		}
		

	}

}
