import Quickshell
import Quickshell.Widgets
import Quickshell.Io 
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme
import qs.modules.panel.components

PanelWindow 
{

	id: panel

	anchors 
    {
		right: true
		bottom: true
		left: true
	}		

	margins 
    {
		right: 	10
		left: 	10
		top: 	0
		bottom: 5
	}

	implicitHeight: 48
	color:		   Theme.Color._invisible
	

	WrapperRectangle 
    {	
		anchors.fill: parent
		color:  Theme.Color._background
		radius: Theme.Style.getMaterialRadius(width, height, "large")

		margin:       10
		leftMargin:   14
		rightMargin:  14

		RowLayout 
        {
			spacing:         10

			Workspaces{}
			Brightness{}
			Audio{}
			Item {Layout.fillWidth: true}
			Battery{}

			Clock{}
			Power{}
		}
	}
}
