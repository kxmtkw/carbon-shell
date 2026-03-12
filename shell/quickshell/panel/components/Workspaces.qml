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
	

	property real workspacesWidth: panel_workspaces_row.implicitWidth
	Layout.preferredWidth: workspacesWidth

	color:  Theme.Color._surfaceContainer
	radius: Theme.Style.getMaterialRadius(width, height, "small")
	

	Behavior on workspacesWidth
	{
		NumberAnimation 
		{
			duration: 100
			easing.type: Easing.InOut
		}
	}

	RowLayout 
	{
		id: panel_workspaces_row
		spacing: 0

		onImplicitWidthChanged: {
			panel_workspaces.workspacesWidth = implicitWidth
		}

		Repeater 
		{
			model: Hyprland.workspaces

			delegate:

			Rectangle 
			{
				Layout.alignment: Qt.AlignVCenter
			
				width:  28
				height: 26
				
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
