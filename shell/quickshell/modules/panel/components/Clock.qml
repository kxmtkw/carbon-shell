import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme

WrapperRectangle
{
    id: panel_clock

	Layout.fillWidth: true
	
    margin: 16
	color:  Theme.Color._surfaceContainer
	radius: Theme.Style.getMaterialRadius(width, height, "small")


	Process
    {
		id: panel_clock_proc
		command: ["date", "+%I%n%M%n%p"]
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
		color: Theme.Color._onSurface
		text:  ""

		horizontalAlignment: Text.AlignHCenter

		font.family:    "Iosevka"
		font.pixelSize: 16
	}
}