import Quickshell
import Quickshell.Widgets
import Quickshell.Hyprland
import QtQuick
import QtQuick.Layouts

import "../material" as Material

import "../global" as Global

PanelWindow {
    
    id: powerMenu

	anchors {
		left: true
		bottom: true
	}		

    margins {
        left: 10
        right: 10
        top: 10
        bottom: 10  
    } 

	implicitWidth: Material.Style.dpi(4800)
    implicitHeight: Material.Style.dpi(5200)
	color: Material.Color.invisible
    visible: Global.State.powerMenuShown


    
    Options{}
    
		
}