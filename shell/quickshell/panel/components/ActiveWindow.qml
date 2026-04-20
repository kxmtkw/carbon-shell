import Quickshell
import Quickshell.Io
import Quickshell.Widgets
import Quickshell.Hyprland
import QtQuick
import QtQuick.Layouts

import qs.Config as Theme

WrapperRectangle
{
    id: panel_activeWindow

    property string activeWindowClass
    property string activeWindowTitle

	property string activeWindowString: activeWindowClass.length > 0 ? 
	activeWindowClass + (activeWindowTitle.length > 0 ? " | " + activeWindowTitle : "") : ""

	Layout.fillHeight: true
	Layout.preferredWidth: 300
	Layout.alignment: Qt.AlignVCenter
	
	color: Theme.Color._invisible

	Connections {
		target: Hyprland
		function onRawEvent(event) {
			if (event.name === "activewindow") {
				const parsed = event.parse(2)
				panel_activeWindow.activeWindowClass = parsed[0]
				panel_activeWindow.activeWindowTitle = parsed[1]
			}
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

		font.family:    Theme.Style.font
		font.pixelSize: 16
		font.weight:    Font.Medium

        elide: Text.ElideRight
	}
}
