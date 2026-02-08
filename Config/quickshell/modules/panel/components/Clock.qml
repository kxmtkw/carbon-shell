import Quickshell
import Quickshell.Widgets
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme

WrapperRectangle
{
	Layout.fillWidth: true
	Layout.alignment: Qt.AlignCenter 
	margin: Theme.Style.dpi(80)
	
	color:  Theme.Color._surfaceContainer
	radius: Theme.Style.roundLess

	SystemClock {
		id: sysclock
		precision: SystemClock.Minutes
	}
	
	Text {
		id:    panelClockText
		color: Theme.Color._onSurface
		text:  Qt.formatDateTime(sysclock.date, "hh\nmm\nAP")

		horizontalAlignment: Text.AlignHCenter

		font.family:    Theme.Font.fontMain
		font.pixelSize: Theme.Style.dpi(250)
	}
}