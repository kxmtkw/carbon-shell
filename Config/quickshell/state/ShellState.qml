pragma Singleton

import QtQuick
import Quickshell

Singleton {
    id: shellState
    property string activeSlider: ""
    
    onActiveSliderChanged: console.log("Active slider changed to:", activeSlider)
    
    signal themeUpdated()
}
