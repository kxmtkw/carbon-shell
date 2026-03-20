import Quickshell
import Quickshell.Widgets
import Quickshell.Services.Notifications
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import qs.Config as Theme


PanelWindow 
{
    id: notifications
    property list<Notification> active_notifications: []


    NotificationServer
    {
        id: notification_server

        keepOnReload: false
        bodyHyperlinksSupported: true
        imageSupported: true
        actionsSupported: true
        bodyMarkupSupported: true
        bodySupported: true

        onNotification: notification => {
            notification.tracked = true
            notifications.active_notifications.push(notification)
        }
    }

    anchors 
    {
		right: true
		bottom: true
	}		

	margins 
    {
		right: 	8
		left: 	8
		top: 	8
		bottom: 8
	}


    exclusiveZone: 0
	implicitWidth: 600
    implicitHeight: notification_container.height
    color: Theme.Color._invisible

    function removeNotification(idx) {
        active_notifications = active_notifications.filter((_, i) => i !== idx)
    }


    ColumnLayout
    {
        id: notification_container
        spacing: 10
        
        Repeater
        {   
            id: notification_container_repeater
            model: notifications.active_notifications

            delegate: Card {
                notifData: modelData

                onClosed: {
                    notifications.removeNotification(index)
                }
            }
        }
        
    }
}