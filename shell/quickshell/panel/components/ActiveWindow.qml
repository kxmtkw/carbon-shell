import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import QtQuick
import QtQuick.Layouts

import qs.theme as Theme

WrapperRectangle
{
    id: panel_activeWindow

    property string activeWindowClass
    property string activeWindowTitle

   property string activeWindowString: activeWindowClass.length > 0 ? activeWindowClass + (activeWindowTitle.length > 0 ? " | " + activeWindowTitle : "") : ""

	Layout.fillHeight: true
	Layout.preferredWidth: 300
	Layout.alignment: Qt.AlignVCenter
	implicitWidth: panel_activeWindow.showingDate ? panel_activeWindow.expanded_width : panel_activeWindow.compressed_width
	
	color: Theme.Color._background



	Process
    {
		id: panel_activeWindow_proc
        command: ["sh", "-c", "hyprctl activewindow -j | jq -r '.class + \":;:;\" + .title'"]
    	running: true
		stdout: StdioCollector {
            onStreamFinished: { 
                panel_activeWindow.activeWindowClass = text.split(":;:;")[0]
                panel_activeWindow.activeWindowTitle = text.split(":;:;")[1]
            }
		}
	}


	Timer
	{
		id: panel_activeWindow_updater
		interval: 100
		running: true
		repeat: true
		onTriggered: {
			if (panel_activeWindow.showingDate) {
				panel_activeWindow_proc_with_date.running = true
			} else {
				panel_activeWindow_proc.running = true
			}
		}
	}

	Timer 
	{
		id: panel_activeWindow_hider
		interval: 3500
		running: panel_activeWindow.showingDate
		onTriggered: {
			panel_activeWindow.showingDate = false
			panel_activeWindow_proc.running = true
		}	
	}
	

	Text 
    {
		id:    panel_activeWindow_text
		anchors.fill: parent
		color: Theme.Color._onSurface
		text:  activeWindowString

		horizontalAlignment: Text.AlignLeft
		verticalAlignment: Text.AlignVCenter

		font.family:    "Iosevka"
		font.pixelSize: 16
		font.weight:    Font.Medium

        elide: Text.ElideRight
	}
}
