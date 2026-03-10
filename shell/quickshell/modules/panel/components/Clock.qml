import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme

WrapperRectangle
{
    id: panel_clock

	Layout.fillHeight: true
	Layout.preferredHeight: 28
	Layout.alignment: Qt.AlignVCenter
	implicitWidth: 96
	
    margin: 8
	color:  Theme.Color._primaryContainer
	radius: Theme.Style.getMaterialRadius(width, height, "small")


	Process
    {
		id: panel_clock_proc
		command: ["date", "+%I:%M %p"]
		running: true
		stdout: StdioCollector {
            onStreamFinished: { panel_clock_text.text = text.trim() }
		}
	}

	Timer
	{
		id: panel_clock_updater
		interval: 1000
		running: true
		repeat: true
		onTriggered: {panel_clock_proc.running = true}
	}
	
	Text 
    {
		id:    panel_clock_text
		anchors.centerIn: parent
		color: Theme.Color._surface
		text:  ""

		horizontalAlignment: Text.AlignHCenter
		verticalAlignment: Text.AlignVCenter

		font.family:    "Iosevka"
		font.pixelSize: 19
	}
}
