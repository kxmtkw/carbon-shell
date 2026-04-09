pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Io

Singleton 
{
    id: style

    property string font
    property string wallpaper

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


    IpcHandler {
        target: "style"

        function update_font(font_name: string): void {
            style.font = font_name
            console.log(font_name)
        }

        function update_wallpaper(path: string): void {
            style.wallpaper = path
            console.log(style.wallpaper)
        }
    }
}