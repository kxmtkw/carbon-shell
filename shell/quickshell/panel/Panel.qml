import Quickshell
import Quickshell.Widgets
import Quickshell.Wayland
import Quickshell.Io 
import QtQuick
import QtQuick.Layouts

import qs.Config as Theme
import qs.panel.components

PanelWindow 
{

	id: panel

	readonly property int modeNormal: 0
	readonly property int modeHidden: 1
	readonly property int modeBypass: 2
	property int panelMode: modeNormal

	WlrLayershell.layer: panelMode === modeBypass ? WlrLayer.Overlay : WlrLayer.Top
	exclusiveZone: panelMode === modeHidden ? 0 : 48

	function setNormalMode() {
		panelMode = modeNormal
	}

	function setHiddenMode() {
		panelMode = modeHidden
	}

	function setBypassMode() {
		panelMode = modeBypass
	}

	anchors 
    {
		right: true
		bottom: true
		left: true
	}		

	margins 
    {
		right: 	8
		left: 	8
		top: 	0
		bottom: panelMode === modeHidden ? 0 : 8
	}

	implicitHeight: panelMode === modeHidden ? 0 : 48
	height: implicitHeight
	color:		   Theme.Color._invisible

	IpcHandler
	{
		target: "panel"

		function normal(): void
		{
			panel.setNormalMode()
		}

		function hidden(): void
		{
			panel.setHiddenMode()
		}

		function bypass(): void
		{
			panel.setBypassMode()
		}
	}

	WrapperRectangle 
    {	
		visible: panel.panelMode !== panel.modeHidden
		anchors.fill: parent
		color:  Theme.Color._background
		radius: Theme.Style.getMaterialRadius(width, height, "large")

		margin:       10
		leftMargin:   14
		rightMargin:  14

		RowLayout 
        {
			spacing:         10

			Launcher{}

			Workspaces{}	
			ActiveWindow{}
			
			Item {Layout.fillWidth: true}

			RowLayout
			{
				spacing: 5
				Wifi{}
				Battery{}
			}

			Clock{}
			Power{}
		}
	}
}
