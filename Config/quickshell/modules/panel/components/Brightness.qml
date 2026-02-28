import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import Quickshell.Services.UPower

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import qs.theme as Theme
import qs.modules.panel as Panel

WrapperRectangle
{
    id: panel_brightness

    Layout.fillWidth:       true
	Layout.alignment:       Qt.AlignHCenter
    margin: 0

    color: Theme.Color._background

	radius: Theme.Style.getMaterialRadius(width, height, "small")

    property bool is_highlighted: false

    ColumnLayout
    {
        spacing: panel_brightness_bar.implicitHeight > 0 || panel_brightness_bar.opacity > 0 ? 10 : 0

        
        Behavior on spacing {
            NumberAnimation
            {
                duration: 100;
                easing.type: Easing.Linear
            }
        }
        
        ProgressBar 
        {
            id: panel_brightness_bar
            from: 0
            to: 100
            value: 0
            Layout.alignment: Qt.AlignHCenter
            implicitWidth: 10
            implicitHeight: 0
            opacity: 0
            topPadding: 0
            bottomPadding: 0


            Behavior on implicitHeight {
                NumberAnimation 
                { 
                    duration: 250; 
                    easing.type: Easing.In
                }
            }

            Behavior on opacity
            {
                NumberAnimation 
                {
                    duration: 250
                    easing.type: Easing.In
                }
            }

            Behavior on value 
            {
                NumberAnimation 
                {
                    duration: 200
                    easing.type: Easing.InOut
                }
            }

            
            contentItem: Rectangle 
            {
                color: Theme.Color._surfaceContainerHigh
                radius: 10
                
                Rectangle 
                {
                    radius: 10
                    width: parent.width
                    height: parent.height * panel_brightness_bar.visualPosition
                    anchors.bottom: parent.bottom
                    color: Theme.Color._primary
                }
            }
        }


        WrapperRectangle
        {
            implicitHeight: 28
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
            color: Theme.Color._surfaceContainer

            MouseArea 
            {
                
                hoverEnabled: true
                Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
                
                Text 
                {
                    id: panel_brightness_icon
                    anchors.centerIn: parent

                    text: ""
                    font.family: "Iosevka"
                    font.pixelSize: 20
                    color: panel_brightness.is_highlighted ? Theme.Color._primary : Theme.Color._onSurface
                    rotation: 0
                }

                onClicked: {
                
                }
                
                onEntered: {
                    parent.color = Theme.Color._surfaceContainer
                }

                onExited: {
                    parent.color = Theme.Color._background
                }
            }
        }
       
    }

    IpcHandler
    {
        target: "brightness"

        function update(amount: int): void { 
            Panel.PanelState.activeSlider = "brightness"
            showBar()
            panel_brightness_bar.value = amount
            panel_brightness_hider.restart()
        }
    }

    Timer
    {
        id: panel_brightness_hider
        interval: 2000
        running: false
        onTriggered: {
            hideBar()
            if (Panel.PanelState.activeSlider === "brightness") {
                Panel.PanelState.activeSlider = ""
            }
        }
    }

    function hideBar(): void {
        panel_brightness.is_highlighted = false
        panel_brightness_bar.implicitHeight = 0
        panel_brightness_bar.opacity = 0
    }

    function showBar(): void {
        panel_brightness.is_highlighted = true
        panel_brightness_bar.implicitHeight = 140
        panel_brightness_bar.opacity = 1
    }

    Connections {
        target: Panel.PanelState
        function onActiveSliderChanged() {
            if (Panel.PanelState.activeSlider !== "brightness") {
                hideBar()
                panel_brightness_hider.stop()
            }
        }
    }

}
