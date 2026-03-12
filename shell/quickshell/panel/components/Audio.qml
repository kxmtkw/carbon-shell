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
    id: panel_audio

    Layout.fillWidth:       false
    Layout.preferredWidth:  28 + panel_audio.sliderWidth + (panel_audio.sliderWidth > 0 ? 8 : 0)
    Layout.preferredHeight: 28
	Layout.alignment:       Qt.AlignVCenter
    margin: 0

    color: Theme.Color._invisible

    radius: Theme.Style.getMaterialRadius(width, height, "small")

    property bool is_muted: false
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
        spacing: panel_audio.sliderWidth > 0 ? 8 : 0
        
        WrapperRectangle
        {
            implicitWidth: 28
            implicitHeight: 28
            Layout.fillWidth: false
            Layout.alignment: Qt.AlignHCenter
            color:  true ? Theme.Color._invisible : Theme.Color._invisible
            radius: Theme.Style.getMaterialRadius(width, height, "small")

            MouseArea
            {
                anchors.fill: parent
                hoverEnabled: true
                

                Text 
                {
                    id: panel_audio_icon
                    anchors.centerIn: parent

                    text: is_muted ? "" : ""
                    font.family: "Iosevka"
                    font.pixelSize: 18
                    color: panel_audio.is_highlighted ? Theme.Color._secondary : Theme.Color._onSurface
                }

                onClicked: {
                    if (ShellState.activeSlider === "audio" && panel_audio_bar.opacity > 0) {
                        ShellState.activeSlider = ""
                        hideBar()
                        panel_audio_hider.stop()
                    } else {
                        ShellState.activeSlider = "audio"
                        showBar()
                        panel_audio_hider.restart()
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
            id: panel_audio_bar
            from: 0
            to: 1
            value: 0
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: panel_audio.sliderWidth
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
                    width: parent.width * panel_audio_bar.visualPosition
                    height: parent.height
                    anchors.left: parent.left
                    color: panel_audio.is_muted ? Theme.Color._secondaryContainer : Theme.Color._secondary
                }

                MouseArea
                {
                    anchors.fill: parent
                    onPressed: panel_audio.setByPosition(mouseX, width)
                    onPositionChanged: {
                        if (pressed) {
                            panel_audio.setByPosition(mouseX, width)
                        }
                    }
                }
            }
        }

    }

    IpcHandler
    {
        target: "audio"

        function update(amount: double): void {
            ShellState.activeSlider = "audio"
            showBar()
            panel_audio_bar.value = amount
            panel_audio_hider.restart()
        }
    }

    Timer
    {
        id: panel_audio_hider
        interval: 2000
        running: false
        onTriggered: {
            hideBar()
            if (ShellState.activeSlider === "audio") {
                ShellState.activeSlider = ""
            }
        }
    }

    function showBar(): void {
        panel_audio.is_highlighted = true
        panel_audio.sliderWidth = 132
        panel_audio_bar.opacity = 1
    }

    function hideBar(): void {
        panel_audio.is_highlighted = false
        panel_audio.sliderWidth = 0
        panel_audio_bar.opacity = 0
    }

    Connections {
        target: ShellState
        function onActiveSliderChanged() {
            if (ShellState.activeSlider !== "audio" && ShellState.activeSlider !== "") {
                hideBar()
                panel_audio_hider.stop()
            }
        }
    }


    Component.onCompleted: pollMutedState()

    Process
    {
        id: panel_audio_mute_process
        command: ["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"]
        running: true

        stdout: StdioCollector
        {
            onStreamFinished: {
                const output = text.trim()
                panel_audio.is_muted = output.indexOf("[MUTED]") !== -1
            }
        }
    }

    Timer
    {
        id: panel_audio_mute_poll
        interval: 200
        running: true
        repeat: true
        onTriggered: panel_audio_mute_process.running = true
    }

    Process
    {
        id: panel_audio_set_process
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

        panel_audio_bar.value = ratio
        panel_audio_set_process.command = ["carbon.audio", "set", ratio.toFixed(2)]
        panel_audio_set_process.running = true

        ShellState.activeSlider = "audio"
        showBar()
        panel_audio_hider.restart()
    }

    function pollMutedState(): void {
        panel_audio_mute_process.running = true
    }
}
