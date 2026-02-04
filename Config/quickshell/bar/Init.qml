import Quickshell
import Quickshell.Widgets
import Quickshell.Io 
import QtQuick
import QtQuick.Layouts

import "../theme" as Theme


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

	implicitWidth: Theme.Style.dpi(740)
	color: Theme.Color._invisible
	

	WrapperRectangle
	{	
		anchors.fill: parent
		color: Theme.Color._background
		radius: Theme.Style.round

		margin: Theme.Style.dpi(140)
		topMargin: Theme.Style.dpi(180)
		bottomMargin: Theme.Style.dpi(180)

		ColumnLayout 
		{
			spacing: Theme.Style.dpi(120)
			anchors.margins: Theme.Style.dpi(0)
			
			Arch {
				Layout.fillWidth: true
				Layout.preferredHeight: Theme.Style.dpi(440)
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
				Layout.preferredHeight: Theme.Style.dpi(440)
				Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
			}

			Clock 
			{
				Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
			}

			Power
			{
				Layout.fillWidth: true
				Layout.preferredHeight: Theme.Style.dpi(440)
				Layout.alignment: Qt.AlignHCenter | Qt.AlignBottom
			}
			
		}
	}
}
