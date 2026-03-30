import QtQuick

Image {
    clip: false
    source: "file:///home/haseeb/Pictures/Wallpapers/pink_city.png"
    x: -(Screen.width - parent.width)
    y: -(Screen.height - parent.height - 54)
    width: Screen.width  
    height: Screen.height 
    fillMode: Image.PreserveAspectCrop
    asynchronous: true
    retainWhileLoading: true
}