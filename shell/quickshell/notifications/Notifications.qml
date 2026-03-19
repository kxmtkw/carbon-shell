import Quickshell
import Quickshell.Widgets
import Quickshell.Services.Notifications
import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

import qs.theme as Theme


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

    function removeNotification(notification) {
        const next = []
        for (const n of notifications.active_notifications) {
            if (n !== notification) next.push(n)
        }
        notifications.active_notifications = next
    }


    ColumnLayout
    {
        id: notification_container
        spacing: 10
        
        Repeater
        {   
            model: notifications.active_notifications

            delegate: Card {
                notifData: modelData

                onClosed: {
                    notifications.removeNotification(modelData)
                }
            }
        }
        
    }
}