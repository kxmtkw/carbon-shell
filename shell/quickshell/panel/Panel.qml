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

	readonly property int positionTop: 0
	readonly property int positionBottom: 1
	property int panelPosition: positionBottom

	WlrLayershell.layer: panelMode === modeBypass ? WlrLayer.Overlay : WlrLayer.Top
	exclusiveZone: implicitHeight

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
		bottom: panelPosition === positionBottom
		top: panelPosition === positionTop
		left: true
	}		

	margins 
    {
		right: 	8
		left: 	8
		top: 	panelMode === modeHidden ? 0 : panelPosition === positionTop ? 8 : 0
		bottom: panelMode === modeHidden ? 0 : panelPosition === positionBottom ? 8 : 0
	}

	implicitHeight: panelMode === modeHidden ? 0 : 46
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
			if (panel.panelMode === panel.modeHidden)
				panel.setNormalMode()
			else
			panel.setHiddenMode()
		}

		function bypass(): void
		{
			if (panel.panelMode === panel.modeBypass)
				panel.setNormalMode()
			else
			panel.setBypassMode()
		}

		function movetotop(): void
		{
			panel.panelPosition = panel.positionTop
		}

		function movetobottom(): void
		{
			panel.panelPosition = panel.positionBottom
		}
	}

	WrapperRectangle 
    {	
		anchors.fill: parent
		color:  Theme.Color._background
		radius: Theme.Style.getMaterialRadius(width, height, "large")

		opacity: panelMode === modeHidden ? 0 : 100

		Behavior on opacity {
			NumberAnimation {
				duration: 200
				easing.type: Easing.OutCubic
			}
		}

		margin:       8
		leftMargin:   16
		rightMargin:  16

		RowLayout 
        {
			spacing:         10

			Workspaces{}	
			ActiveWindow{}

			Launcher{
				Layout.fillWidth: true
			}
			
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
