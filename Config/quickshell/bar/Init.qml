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
		anchors.fill: parent
		spacing: Material.Style.dpi(160)
		anchors.margins: Material.Style.dpi(100)

		

		Workspaces {
			Layout.fillWidth: true
			Layout.preferredHeight: Material.Style.dpi(2200)
			Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
		}

		Item 
		{
			Layout.fillHeight: true
		}

		Clock 
		{
			Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
		}

		Power
		{
			Layout.fillWidth: true
			Layout.preferredHeight: Material.Style.dpi(360)
			Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
		}
		
	}

	
}
