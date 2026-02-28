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
    id: panel_audio

    Layout.fillWidth:       true
	Layout.alignment:       Qt.AlignHCenter
    margin: 0

    color: Theme.Color._background

	radius: Theme.Style.getMaterialRadius(width, height, "small")

    property bool is_muted: false
    property bool is_highlighted: false

    ColumnLayout
    {
        spacing: panel_audio_bar.implicitHeight > 0 || panel_audio_bar.opacity > 0 ? 10 : 0

        Behavior on spacing {
            NumberAnimation
            {
                duration: 100;
                easing.type: Easing.Linear
            }
        }
        
        ProgressBar 
        {
            id: panel_audio_bar
            from: 0
            to: 1
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
                    height: parent.height * panel_audio_bar.visualPosition
                    anchors.bottom: parent.bottom
                    color: panel_audio.is_muted ? Theme.Color._secondaryContainer : Theme.Color._secondary
                }
            }
        }

        MouseArea 
        {
            implicitHeight: 28
            hoverEnabled: true
            Layout.alignment: Qt.AlignTop | Qt.AlignHCenter
            
            Text 
            {
                id: panel_audio_icon
                anchors.centerIn: parent

                text: is_muted ? "" : ""
                font.family: "Iosevka"
                font.pixelSize: 20
                color: panel_audio.is_highlighted ? Theme.Color._secondary : Theme.Color._onSurface
            }
        }
    }

    IpcHandler
    {
        target: "audio"

        function update(amount: double): void {
            Panel.PanelState.activeSlider = "audio"
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
            if (Panel.PanelState.activeSlider === "audio") {
                Panel.PanelState.activeSlider = ""
            }
        }
    }

    function showBar(): void {
        panel_audio.is_highlighted = true
        panel_audio_bar.implicitHeight = 140
        panel_audio_bar.opacity = 1
    }

    function hideBar(): void {
        panel_audio.is_highlighted = false
        panel_audio_bar.implicitHeight = 0
        panel_audio_bar.opacity = 0
    }

    Connections {
        target: Panel.PanelState
        function onActiveSliderChanged() {
            if (Panel.PanelState.activeSlider !== "audio") {
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
}
