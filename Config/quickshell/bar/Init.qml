import Quickshell
import Quickshell.Widgets
import Quickshell.Io 
import QtQuick
import QtQuick.Layouts

import "../material" as Material


PanelWindow {

	anchors {
		top: true
		left: true
		bottom: true
	}		

	implicitWidth: Material.Style.dpi(600)

	color: Material.Color.background
	

	ColumnLayout
	{
		anchors.centerIn: parent
		spacing: Material.Style.dpi(400)

		Clock{}
	}
}

1