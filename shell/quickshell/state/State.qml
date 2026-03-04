pragma Singleton

import QtQuick
import Quickshell

Singleton {
    property string activeSlider: ""
    
    signal themeUpdated()
}
