import QtQuick
import QtQuick.Effects
import QtQuick.Layouts
import QtQuick.Shapes
import Quickshell
import Quickshell.Widgets

PanelWindow {
    id: window
    color: "transparent"
    visible: true
    width: 600
    height: 200
    contentItem.layer.enabled: true
    exclusiveZone: 0
    margins {
        bottom: 0
    }
    anchors {
        bottom: true
        right: true
    }
    
    Item {
        id: mask
        visible: false
        layer.enabled: true
        anchors.fill: parent
        
        Item {
            anchors.fill: parent
            
            // Top-left normal radius
            Rectangle {
                anchors.fill: parent
                topLeftRadius: 20
            }
            
            // Top-right notch
            Shape {
                anchors.top: parent.top
                anchors.right: parent.right
                width: 16
                height: 16
                
                ShapePath {
                    startX: 0
                    startY: 0
                    strokeWidth: -1
                    fillColor: "white"
                    
                    PathArc {
                        x: 16
                        y: 16
                        radiusX: 16
                        radiusY: 16
                    }
                    
                    PathLine { x: 16; y: 0 }
                }
                
                transform: Rotation {
                    origin.x: 8
                    origin.y: 8
                    angle: 90
                }
            }
            
            // Bottom-left notch
            Shape {
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                width: 16
                height: 16
                
                ShapePath {
                    startX: 0
                    startY: 0
                    strokeWidth: -1
                    fillColor: "white"
                    
                    PathArc {
                        x: 16
                        y: 16
                        radiusX: 16
                        radiusY: 16
                    }
                    
                    PathLine { x: 16; y: 0 }
                }
                
                transform: Rotation {
                    origin.x: 8
                    origin.y: 8
                    angle: 270
                }
            }
        }
    }
    
    contentItem.layer.effect: MultiEffect {
        maskEnabled: true
        maskSource: mask
        maskSpreadAtMin: 1
        maskThresholdMin: 0.5
    }
    

    WallpaperImage{}

    
    WrapperRectangle {
        anchors.fill: parent
        color: '#00000000'
        margin: 12  
        
        Card{}
    }
}