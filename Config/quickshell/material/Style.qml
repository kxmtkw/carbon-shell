
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

	property real roundNone:              dpi(0)
	property real roundExtraSmall:        dpi(4) 
	property real roundSmall:             dpi(8)
	property real roundMedium:            dpi(12)
	property real roundLarge:             dpi(16)
	property real roundLargeInc:          dpi(20)
	property real roundExtraLarge:        dpi(28)
	property real roundExtraLargeInc:     dpi(32)
	property real roundExtraExtraLarge:   dpi(48)
	property real roundFull:              dpi(60)

	function round(round_value, width, height) 
	{
		return round_value * (Math.min(width, height) / 8)
	}
}
