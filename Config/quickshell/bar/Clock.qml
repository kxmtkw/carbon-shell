import Quickshell
import Quickshell.Widgets
import QtQuick

import "../theme" as Theme

WrapperRectangle
{
	margin: Theme.Style.dpi(70)
	topMargin: Theme.Style.dpi(120)

	color: Theme.Color._surfaceContainer
	radius: Theme.Style.roundLess

	SystemClock {
		id: sysclock
		precision: SystemClock.Minutes
	}
	
	Text {
		id: barClock
		anchors.centerIn: parent
		color: Theme.Color._onSurface
		text: Qt.formatDateTime(sysclock.date, "hh\nmm\nAP")
	}
}