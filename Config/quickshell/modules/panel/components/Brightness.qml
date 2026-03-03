import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import Quickshell.Services.UPower

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import qs.theme as Theme
import qs.state

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

                MouseArea
                {
                    anchors.fill: parent
                    onPressed: panel_brightness.setByPosition(mouseY, height)
                    onPositionChanged: {
                        if (pressed) {
                            panel_brightness.setByPosition(mouseY, height)
                        }
                    }
                }
            }
        }


        WrapperRectangle
        {
            implicitHeight: 28
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
            color: Theme.Color._background
            radius: Theme.Style.getMaterialRadius(width, height, "small")


            MouseArea 
            {
                anchors.fill: parent
                hoverEnabled: true
                
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
                    if (ShellState.activeSlider === "brightness" && panel_brightness_bar.opacity > 0) {
                        ShellState.activeSlider = ""
                        ShellState.activeSliderChanged("")
                        hideBar()
                        panel_brightness_hider.stop()
                    } else {
                        ShellState.activeSlider = "brightness"
                        ShellState.activeSliderChanged("brightness")
                        showBar()
                        panel_brightness_hider.restart()
                    }
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
            ShellState.activeSlider = "brightness"
            ShellState.activeSliderChanged("brightness")
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
            if (ShellState.activeSlider === "brightness") {
                ShellState.activeSlider = ""
                ShellState.activeSliderChanged("")
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
        target: ShellState
        function onActiveSliderChanged() {
            if (ShellState.activeSlider !== "brightness" && ShellState.activeSlider !== "") {
                hideBar()
                panel_brightness_hider.stop()
            }
        }
    }

    Process
    {
        id: panel_brightness_set_process
        running: false
        command: []
    }

    function setByPosition(y: real, totalHeight: real): void {
        var ratio = 1 - (y / totalHeight)
        if (ratio < 0) ratio = 0
        if (ratio > 1) ratio = 1

        var target = Math.round(ratio * 100)

        if (target <= 10) {
            target = 10
        }
        
        panel_brightness_bar.value = target

        console.log(target)
        panel_brightness_set_process.command = ["carbon.brightness", "set", target.toString()]
        panel_brightness_set_process.running = true

        ShellState.activeSlider = "brightness"
        ShellState.activeSliderChanged("brightness")
        panel_brightness_hider.restart()
    }

}
