import Quickshell
import Quickshell.Widgets
import Quickshell.Io 
import QtQuick
import QtQuick.Layouts

import "../material" as Material


PanelWindow {

	anchors 
	{
		top: true
		left: true
		bottom: true
	}		

	margins
	{
		right: 0
		left: 8
		top: 8
		bottom: 8
	}

	implicitWidth: Material.Style.dpi(600)
	color: Material.Color.invisible
	

	WrapperRectangle
	{	
		anchors.fill: parent
		color: Material.Color.background
		radius: Material.Style.round(Material.Style.roundExtraLargeInc, width, height)

		margin: Material.Style.dpi(120)
		topMargin: Material.Style.dpi(160)
		bottomMargin: Material.Style.dpi(160)

		ColumnLayout 
		{
			
			spacing: Material.Style.dpi(160)
			anchors.margins: Material.Style.dpi(100)
			
			Arch {
				Layout.fillWidth: true
				Layout.preferredHeight: Material.Style.dpi(360)
				Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom	
			}
			

			Workspaces {
				Layout.fillWidth: true
				Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
			}

			Item 
			{
				Layout.fillHeight: true
			}

			Battery
			{
				Layout.fillWidth: true
				Layout.preferredHeight: Material.Style.dpi(360)
				Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
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
}
