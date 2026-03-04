pragma Singleton

import QtQuick
import Quickshell
import Quickshell.Io

Singleton {
    id: themeColor

    property var _colors: ({})

    function _color(name) {
        const value = _colors[name]
        return typeof value === "string" ? value : "#00000000"
    }

    function _applyFromFile() {
        try {
            const raw = color_file.text()
            const parsed = JSON.parse(raw)
            if (parsed && typeof parsed === "object") {
                _colors = parsed
            }
        } catch (e) {
            console.error("Failed to load theme/color.json:", e)
        }
    }

    function reloadFromJson() {
        color_file.reload()
        apply_timer.restart()
    }

        FileView {
        id: color_file
        path: Qt.resolvedUrl("./color.json")
    }

    Timer {
        id: apply_timer
        interval: 25
        repeat: false
        onTriggered: themeColor._applyFromFile()
    }

    IpcHandler {
        target: "theme"

        function update(): void {
            themeColor.reloadFromJson()
        }
    }

    Component.onCompleted: reloadFromJson()


    property color _invisible: _color("invisible")

    property color _background: _color("background")
    property color _backgroundTransparentxAA: _color("backgroundTransparentxAA")
    property color _backgroundTransparentAAx: _color("backgroundTransparentAAx")
    property color _surface: _color("surface")
    property color _surfaceDim: _color("surfaceDim")
    property color _surfaceBright: _color("surfaceBright")
    property color _surfaceContainerLowest: _color("surfaceContainerLowest")
    property color _surfaceContainerLow: _color("surfaceContainerLow")
    property color _surfaceContainer: _color("surfaceContainer")
    property color _surfaceContainerHigh: _color("surfaceContainerHigh")
    property color _surfaceContainerHighest: _color("surfaceContainerHighest")
    property color _onSurface: _color("onSurface")
    property color _surfaceVariant: _color("surfaceVariant")
    property color _onSurfaceVariant: _color("onSurfaceVariant")
    property color _inverseSurface: _color("inverseSurface")
    property color _inverseOnSurface: _color("inverseOnSurface")
    property color _outline: _color("outline")
    property color _outlineVariant: _color("outlineVariant")
    property color _shadow: _color("shadow")
    property color _scrim: _color("scrim")
    property color _surfaceTint: _color("surfaceTint")
    property color _primary: _color("primary")
    property color _onPrimary: _color("onPrimary")
    property color _primaryContainer: _color("primaryContainer")
    property color _onPrimaryContainer: _color("onPrimaryContainer")
    property color _inversePrimary: _color("inversePrimary")
    property color _secondary: _color("secondary")
    property color _onSecondary: _color("onSecondary")
    property color _secondaryContainer: _color("secondaryContainer")
    property color _onSecondaryContainer: _color("onSecondaryContainer")
    property color _tertiary: _color("tertiary")
    property color _onTertiary: _color("onTertiary")
    property color _tertiaryContainer: _color("tertiaryContainer")
    property color _onTertiaryContainer: _color("onTertiaryContainer")
    property color _error: _color("error")
    property color _onError: _color("onError")
    property color _errorContainer: _color("errorContainer")
    property color _onErrorContainer: _color("onErrorContainer")
    property color _primaryFixed: _color("primaryFixed")
    property color _primaryFixedDim: _color("primaryFixedDim")
    property color _onPrimaryFixed: _color("onPrimaryFixed")
    property color _onPrimaryFixedVariant: _color("onPrimaryFixedVariant")
    property color _secondaryFixed: _color("secondaryFixed")
    property color _secondaryFixedDim: _color("secondaryFixedDim")
    property color _onSecondaryFixed: _color("onSecondaryFixed")
    property color _onSecondaryFixedVariant: _color("onSecondaryFixedVariant")
    property color _tertiaryFixed: _color("tertiaryFixed")
    property color _tertiaryFixedDim: _color("tertiaryFixedDim")
    property color _onTertiaryFixed: _color("onTertiaryFixed")
    property color _onTertiaryFixedVariant: _color("onTertiaryFixedVariant")
    property color _red: _color("red")
    property color _blue: _color("blue")
    property color _yellow: _color("yellow")
    property color _orange: _color("orange")
    property color _green: _color("green")
    property color _cyan: _color("cyan")
    property color _magenta: _color("magenta")
    property color _white: _color("white")
    property color _black: _color("black")
}
