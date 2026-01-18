
pragma Singleton

import QtQuick
import QtQuick.Window
import Quickshell

Singleton 
{
	function dpi(num) 
	{
		return num * (Screen.pixelDensity / 80);
	}

	property real roundNone:              0
	property real roundExtraSmall:        4 
	property real roundSmall:             8
	property real roundMedium:            12
	property real roundLarge:             16
	property real roundLargeInc:          20
	property real roundExtraLarge:        28
	property real roundExtraLargeInc:     32
	property real roundExtraExtraLarge:   48
	property real roundFull:              60

	function round(round_value, width, height) 
	{
		return round_value * (Math.min(width, height) / dpi(1500))
	}


	function setOpacity(hexColor, opacity) {

		opacity = Math.max(0, Math.min(1, opacity))

		let alpha = Math.round(opacity * 255)
			.toString(16)
			.padStart(2, "0")

		hex = hexColor.replace("#", "")

		return "#" + alpha + hex
	}
}

