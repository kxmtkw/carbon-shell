import Quickshell
import Quickshell.Widgets
import QtQuick

import "../material" as Material

WrapperRectangle
{
	margin: Material.Style.dpi(70)
	topMargin: Material.Style.dpi(120)

	color: Material.Color._surfaceContainer
	radius: Material.Style.round(Material.Style.roundExtraLargeInc, width, height)

	SystemClock {
		id: sysclock
		precision: SystemClock.Minutes
	}
	
	Text {
		id: barClock
		anchors.centerIn: parent
		color: Material.Color._onSurface
		text: Qt.formatDateTime(sysclock.date, "hh\nmm\nAP")
	}
}