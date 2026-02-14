import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme



WrapperRectangle
{
	Layout.fillWidth:        true
	Layout.preferredHeight: Theme.Style.dpi(440)
	Layout.alignment:       Qt.AlignHCenter

	margin: Theme.Style.dpi(70)
	color:  Theme.Color._background
	radius: Theme.Style.round

	Process 
	{
		id: power_menu
		running: false
		command: ["sh", "-c", "~/.carbon/controllers/launch.sh wifi"]
	}

	MouseArea
	{
		Layout.fillHeight: true
		Layout.fillWidth:  true

		hoverEnabled: true 

		Text
		{
			id: panelWifiIcon
			anchors.centerIn: parent
			
			text: ""

			font.family:    Theme.Font.fontMain
			font.pixelSize: Theme.Style.dpi(300)
			color:          Theme.Color._onSurface

		}

		onClicked: {
			power_menu.running = true
		}

		onEntered: {
			parent.color = Theme.Color._surfaceContainerLow
		}

		onExited: {
			parent.color = Theme.Color._background
		}

	}
}