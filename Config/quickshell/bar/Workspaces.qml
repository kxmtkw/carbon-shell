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

	color: Material.Color.surface_container

	radius: Material.Style.round(Material.Style.roundLargeInc, width, height)

	
	
	ColumnLayout {
		anchors.centerIn: parent
		spacing: 6

		Repeater {
			model: Hyprland.workspaces

			delegate:

			Rectangle {
				Layout.alignment: Qt.AlignHCenter

				width: Material.Style.dpi(180)
				height: Material.Style.dpi(180)
				
				radius: Material.Style.round(Material.Style.roundExtraLarge, width, height)
				color: modelData.focused ? Material.Color.primary_container : Material.Color.surface_dim 
			}
			
		}



	}
}