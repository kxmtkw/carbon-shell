pragma Singleton

import QtQuick
import Quickshell

Singleton 
{
	function getMaterialRadius(width, height, shapeSetting) 
    {
        const shorter = Math.min(width, height)

        switch (shapeSetting) 
        {
            case "none":        return 0
            case "extra-small": return Math.min(4, shorter / 2)
            case "small":       return Math.min(8, shorter / 2)
            case "medium":      return Math.min(12, shorter / 2)
            case "large":       return Math.min(16, shorter / 2)
            case "extra-large": return Math.min(28, shorter / 2)
            case "full":        return shorter / 2
            default:
                console.warn("Unknown shape setting:", shapeSetting)
                return 0
        }

    }
}