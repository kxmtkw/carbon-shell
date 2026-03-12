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

    Layout.fillWidth:       false
    Layout.preferredWidth:  28 + panel_brightness.sliderWidth + (panel_brightness.sliderWidth > 0 ? 8 : 0)
    Layout.preferredHeight: 28
	Layout.alignment:       Qt.AlignVCenter
    margin: 0

    color: Theme.Color._invisible

    radius: Theme.Style.getMaterialRadius(width, height, "small")

    property bool is_highlighted: false
    property real sliderWidth: 0

    Behavior on sliderWidth {
        NumberAnimation {
            duration: 220
            easing.type: Easing.InOutQuad
        }
    }

    RowLayout
    {
        anchors.centerIn: parent
        spacing: panel_brightness.sliderWidth > 0 ? 8 : 0


        WrapperRectangle
        {
            implicitWidth: 28
            implicitHeight: 28
            Layout.fillWidth: false
            Layout.alignment: Qt.AlignHCenter
            color: Theme.Color._invisible
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
                        hideBar()
                        panel_brightness_hider.stop()
                    } else {
                        ShellState.activeSlider = "brightness"
                        showBar()
                        panel_brightness_hider.restart()
                    }
                }
                
                onEntered: {
                    parent.color = Theme.Color._surfaceContainer
                }

                onExited: {
                    parent.color = Theme.Color._invisible
                }
            }
        }
     
        
        ProgressBar 
        {
            id: panel_brightness_bar
            from: 0
            to: 100
            value: 0
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: panel_brightness.sliderWidth
            implicitHeight: 10
            opacity: 0
            topPadding: 0
            bottomPadding: 0

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
                    duration: 150
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
                    width: parent.width * panel_brightness_bar.visualPosition
                    height: parent.height
                    anchors.left: parent.left
                    color: Theme.Color._primary
                }

                MouseArea
                {
                    anchors.fill: parent
                    onPressed: panel_brightness.setByPosition(mouseX, width)
                    onPositionChanged: {
                        if (pressed) {
                            panel_brightness.setByPosition(mouseX, width)
                        }
                    }
                }
            }
        }
  
    }

    IpcHandler
    {
        target: "brightness"

        function update(amount: int): void { 
            ShellState.activeSlider = "brightness"
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
            }
        }
    }

    function hideBar(): void {
        panel_brightness.is_highlighted = false
        panel_brightness.sliderWidth = 0
        panel_brightness_bar.opacity = 0
    }

    function showBar(): void {
        panel_brightness.is_highlighted = true
        panel_brightness.sliderWidth = 132
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

    function setByPosition(x: real, totalWidth: real): void {
        if (totalWidth <= 0) {
            return
        }

        var ratio = x / totalWidth
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
        panel_brightness_hider.restart()
    }

}
