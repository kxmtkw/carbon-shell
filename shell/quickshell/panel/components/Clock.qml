import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme

WrapperRectangle
{
    id: panel_clock

	property bool showingDate: false

	property real compressed_width: 100
	property real expanded_width: 240

	Layout.fillHeight: true
	Layout.preferredHeight: 28
	Layout.alignment: Qt.AlignVCenter
	implicitWidth: panel_clock.showingDate ? panel_clock.expanded_width : panel_clock.compressed_width
	
    margin: 8
	color: Theme.Color._primaryContainer
	radius: Theme.Style.getMaterialRadius(width, height, "small")


	Behavior on implicitWidth
	{
		NumberAnimation 
		{
			duration: 200
			easing.type: Easing.InOut
		}
	}

	Process
    {
		id: panel_clock_proc
		command: ["date", "+%I:%M %p"]
		running: true
		stdout: StdioCollector {
            onStreamFinished: { panel_clock_text.text = text.trim() }
		}
	}

	Process
    {
		id: panel_clock_proc_with_date
		command: ["date", "+%I:%M %p | %a | %d %b "]
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
		onTriggered: {
			if (panel_clock.showingDate) {
				panel_clock_proc_with_date.running = true
			} else {
				panel_clock_proc.running = true
			}
		}
	}

	Timer 
	{
		id: panel_clock_hider
		interval: 3500
		running: panel_clock.showingDate
		onTriggered: {
			panel_clock.showingDate = false
			panel_clock_proc.running = true
		}	
	}
	

	Text 
    {
		id:    panel_clock_text
		anchors.fill: parent
		color: Theme.Color._surface
		text:  ""

		horizontalAlignment: Text.AlignHCenter
		verticalAlignment: Text.AlignVCenter

		font.family:    "Iosevka"
		font.pixelSize: 19
		font.weight:    Font.Medium

		MouseArea
		{
			anchors.fill: parent
			cursorShape: Qt.PointingHandCursor

			onReleased: {
				panel_clock.showingDate = !panel_clock.showingDate

				if (panel_clock.showingDate) {
					panel_clock_proc_with_date.running = true
				} else {
					panel_clock_proc.running = true
				}
			}
		}
	}
}
