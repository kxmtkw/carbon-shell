
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
	property real round:              dpi(140);
	property real roundMore:          dpi(260);


	function brighten(color, factor) 
	{
		var r = color.r * 255
		var g = color.g * 255
		var b = color.b * 255

		r = Math.min(255, r + (255 - r) * factor)
		g = Math.min(255, g + (255 - g) * factor)
		b = Math.min(255, b + (255 - b) * factor)

		return Qt.rgba(r / 255, g / 255, b / 255, color.a)
	}



}

