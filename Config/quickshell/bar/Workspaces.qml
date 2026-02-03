import Quickshell
import Quickshell.Widgets
import Quickshell.Hyprland
import QtQuick
import QtQuick.Layouts

import "../material" as Material


WrapperRectangle
{
	margin: Material.Style.dpi(70)
	topMargin: Material.Style.dpi(120)

	color: Material.Color._surfaceContainer

	radius: Material.Style.round(Material.Style.roundExtraLargeInc, width, height)

	
	
	ColumnLayout {
		anchors.centerIn: parent
		spacing: Material.Style.dpi(120)

		Repeater {
			model: Hyprland.workspaces

			delegate:

			Rectangle {
				Layout.alignment: Qt.AlignHCenter

				width: Material.Style.dpi(200)
				height: Material.Style.dpi(200)
				
				radius: Material.Style.round(Material.Style.roundExtraLargeInc, width, height)
				color: modelData.focused ? Material.Color._tertiaryContainer : Material.Color._background


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