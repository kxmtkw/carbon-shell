import Quickshell
import Quickshell.Widgets
import Quickshell.Io 
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme
import qs.modules.panel.components

PanelWindow {

	id: panel

	anchors {
		top: true
		left: true
		bottom: true
	}		

	margins {
		right: 	Theme.Style.dpi(0)
		left: 	Theme.Style.dpi(120)
		top: 	Theme.Style.dpi(120)
		bottom: Theme.Style.dpi(120)
	}

	implicitWidth: Theme.Style.dpi(740)
	color:		   Theme.Color._invisible
	

	WrapperRectangle {	
		anchors.fill: parent
		color:  Theme.Color._background
		radius: Theme.Style.round

		margin:       Theme.Style.dpi(140)
		topMargin:    Theme.Style.dpi(220)
		bottomMargin: Theme.Style.dpi(220)

		ColumnLayout {
			spacing:         Theme.Style.dpi(180)
			
			Arch{}
			Workspaces{}
			Player{}
				
			Item {Layout.fillHeight: true}
			
			ColumnLayout {	
				spacing: Theme.Style.dpi(40)

				Battery{}
				Wifi{}
			}

			Clock{}
			Power{}
		}
	}
}
