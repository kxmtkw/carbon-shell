import Quickshell
import Quickshell.Widgets
import Quickshell.Hyprland
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme


WrapperRectangle
{
	margin: Theme.Style.dpi(70)
	topMargin: Theme.Style.dpi(200)
	bottomMargin: Theme.Style.dpi(200)

	color: Theme.Color._surfaceContainer

	radius: Theme.Style.roundLess

	
	
	ColumnLayout {
		anchors.centerIn: parent
		spacing: Theme.Style.dpi(140)

		Repeater {
			model: Hyprland.workspaces

			delegate:

			Rectangle {
				Layout.alignment: Qt.AlignHCenter

				width: Theme.Style.dpi(240)
				height: Theme.Style.dpi(240)
				
				radius: Theme.Style.roundLesser
				color: modelData.focused ? Theme.Color._tertiaryContainer : Theme.Color._background


				MouseArea
				{
					anchors.fill: parent
					hoverEnabled: true
					onEntered: {modelData.activate()}
				}
			}
			
		}



	}
}