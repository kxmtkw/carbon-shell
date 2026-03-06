import Quickshell
import Quickshell.Widgets
import Quickshell.Hyprland
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme


WrapperRectangle
{
	id: panel_workspaces
	Layout.fillHeight: true
	Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft
	
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

	RowLayout 
	{
		anchors.centerIn: parent
		spacing: 0

		Repeater 
		{
			model: Hyprland.workspaces

			delegate:

			Rectangle 
			{
				Layout.alignment: Qt.AlignVCenter

				width:  28
				height: 24
				
				radius: Theme.Style.getMaterialRadius(width, height, "small")
				color:  modelData.active ? Theme.Color._tertiaryContainer : Theme.Color._invisible

				
				Text
				{
					anchors.centerIn: parent
					color: modelData.active ? Theme.Color._onTertiaryContainer : Theme.Color._invisible
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
