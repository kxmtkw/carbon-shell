
pragma Singleton

import QtQuick
import QtQuick.Window
import Quickshell

Singleton 
{
	function dpi(num) 
	{
		return num * (Screen.pixelDensity / 96);
	}

	property real roundLesser:        dpi(40);
	property real roundLess:          dpi(80);
	property real round:              dpi(160);
	property real roundMore:          dpi(260);


	function setOpacity(hexColor, opacity) {

		opacity = Math.max(0, Math.min(1, opacity))

		let alpha = Math.round(opacity * 255)
			.toString(16)
			.padStart(2, "0")

		hex = hexColor.replace("#", "")

		return "#" + alpha + hex
	}
}

