import Quickshell
import Quickshell.Widgets
import Quickshell.Io 
import QtQuick
import QtQuick.Layouts

import qs.Config as Theme
import qs.panel.components

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
		right: 	8
		left: 	8
		top: 	0
		bottom: 8
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
