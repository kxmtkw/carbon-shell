import Quickshell
import Quickshell.Widgets
import Quickshell.Io 
import Quickshell.Hyprland
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme

PanelWindow {
    
	id: window
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

	implicitWidth: Theme.Style.dpi(8000)
	color: Theme.Color._invisible
    exclusiveZone: 0 
    visible: true
    focusable: true
	

	WrapperRectangle
	{	
		anchors.fill: parent
		color: Theme.Color._background
		radius: Theme.Style.round

		margin: Theme.Style.dpi(140)
		topMargin: Theme.Style.dpi(180)
		bottomMargin: Theme.Style.dpi(180)
	}

	HyprlandFocusGrab {
		windows: [ window ]
		active: true
		onCleared:
		{
			window.visible = false
		}
    }

	
}
