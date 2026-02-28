import Quickshell
import Quickshell.Widgets
import Quickshell.Hyprland
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme


WrapperRectangle
{
	id: panel_workspaces
	Layout.fillWidth: true
	Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
	
	margin: 0

	color:  Theme.Color._surfaceContainer
	radius: Theme.Style.getMaterialRadius(width, height, "medium")
	

	Behavior on height
	{
		NumberAnimation 
		{
			duration: 250
			easing.type: Easing.InOut
		}
	}

	ColumnLayout 
	{
		anchors.centerIn: parent
		spacing: 0

		Repeater 
		{
			model: Hyprland.workspaces

			delegate:

			Rectangle 
			{
				Layout.fillWidth: true
				Layout.alignment: Qt.AlignHCenter

				width:  16
				height: 28
				
				radius: Theme.Style.getMaterialRadius(width, height, "small")
				color:  modelData.focused ? Theme.Color._tertiaryContainer : Theme.Color._surfaceContainer

				
				Text
				{
					anchors.centerIn: parent
					color: modelData.focused ? Theme.Color._onTertiaryContainer : Theme.Color._surfaceContainer
					text: modelData.id
				}

				MouseArea
				{
					anchors.fill: parent
					hoverEnabled: true
					onClicked:   {modelData.activate()}
				}
			}
			
		}
	}
}