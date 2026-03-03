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
		top: true
		bottom: true
		left: true
	}		

	margins 
    {
		right: 	0
		left: 	10
		top: 	10
		bottom: 10
	}

	implicitWidth: 48
	color:		   Theme.Color._invisible
	

	WrapperRectangle 
    {	
		anchors.fill: parent
		color:  Theme.Color._background
		radius: Theme.Style.getMaterialRadius(width, height, "large")

		margin:       10
		topMargin:    24
		bottomMargin: 24

		ColumnLayout 
        {
			spacing:         16

			Workspaces{}
			
			ColumnLayout
			{
				spacing: 10
				
				Brightness{}
				Audio{}
			}
			
			Item {Layout.fillHeight: true}

			ColumnLayout
			{	
				Battery{}
			}

			Clock{}
		}
	}
}
