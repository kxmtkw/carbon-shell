import Quickshell
import Quickshell.Widgets
import Quickshell.Io
import QtQuick
import QtQuick.Effects
import QtQuick.Layouts
import QtQuick.Shapes


import qs.Config as Theme

PanelWindow
{
	id: notif

	property var queue: []
	property bool showing: false
	property int defaultTimeout: 5000

	property int notifId: 0
	property int replacesId: 0
	property string appName: ""
	property string appIcon: ""
	property string summary: ""
	property string body: ""
	property int urgency: 0
	property string image: ""
	property int expireTimeout: -1

	anchors
	{
		bottom: true
	}

	margins
	{
		bottom: 2
	}

	implicitWidth: 620
	implicitHeight: notif_card.implicitHeight + 20
	height: implicitHeight
	color: Theme.Color._invisible
	exclusiveZone: 0
	visible: showing


	WrapperRectangle
	{
		id: notif_card
		implicitHeight: content_column.implicitHeight + 40
		opacity: 0
		anchors.fill: parent
		anchors.margins: 8
		color: Theme.Color._background
		radius: Theme.Style.getMaterialRadius(width, height, "extra-large")
		border.width: 4
		border.color: notif.urgency == 2 ? Theme.Color._error : Theme.Color._primary

		Column
		{
			id: content_column
			anchors
			{
				top: parent.top
				left: parent.left
				right: parent.right
				margins: 20
			}

			spacing: 5

			RowLayout
			{
				width: parent.width
				spacing: 6

				Image
				{
					visible: appIcon !== ""
					source: appIcon
					height: 22
					width: 22
					Layout.alignment: Qt.AlignVCenter
					smooth: true
				}

				Text
				{
					text: appName
					font.pixelSize: 14
					font.italic: true
					color: Theme.Color._onSurface
					Layout.fillWidth: true
					Layout.alignment: Qt.AlignVCenter
					elide: Text.ElideRight
				}

				Item
				{
					width: 18
					height: 18
					Layout.alignment: Qt.AlignVCenter

					Text
					{
						anchors.centerIn: parent
						text: ""
						font.pixelSize: 16
						color: Theme.Color._onSurface
					}

					MouseArea
					{
						anchors.fill: parent
						cursorShape: Qt.PointingHandCursor
						onClicked: {
							hide_timer.stop()
							_showNext()
						}
					}
				}
			}

			RowLayout
			{
				width: parent.width
				spacing: 20

				Item
				{
					visible: (image !== "" || appIcon !== "")
					implicitWidth: 180
					implicitHeight: 180

					Rectangle
					{
						anchors.fill: parent
						color: "transparent"
						radius: 10
						clip: true
						layer.enabled: true
						layer.smooth: true

						Image
						{
							anchors.fill: parent
							source: image !== "" ? image : appIcon
							sourceSize.width: 320
							sourceSize.height: 320
							fillMode: Image.PreserveAspectFit
							mipmap: true
							smooth: true
						}
					}
				}

				ColumnLayout
				{
					Layout.fillWidth: true
					spacing: 5

					Text
					{
						text: summary
						font.pixelSize: 22
						font.weight: Font.Medium
						color: Theme.Color._onSurface
						Layout.fillWidth: true
						wrapMode: Text.WrapAtWordBoundaryOrAnywhere
						maximumLineCount: 1
					}

					Text
					{
						text: body
						font.pixelSize: 14
						color: Theme.Color._onSurface
						Layout.fillWidth: true
						wrapMode: Text.WrapAtWordBoundaryOrAnywhere
						visible: body !== ""
					}
				}
			}
		}
	}

	SequentialAnimation
	{
		id: swap_anim
		running: false

		ParallelAnimation
		{
			PropertyAnimation
			{
				target: notif_card
				property: "opacity"
				to: 0
				duration: 120
				easing.type: Easing.OutQuad
			}
			PropertyAnimation
			{
				target: notif_card
				property: "y"
				to: 8
				duration: 120
				easing.type: Easing.OutQuad
			}
		}

		ScriptAction
		{
			script: {
				if (pendingNotification) {
					_applyNotification(pendingNotification)
				}
			}
		}

		ParallelAnimation
		{
			PropertyAnimation
			{
				target: notif_card
				property: "opacity"
				to: 1
				duration: 160
				easing.type: Easing.OutQuad
			}
			PropertyAnimation
			{
				target: notif_card
				property: "y"
				to: 0
				duration: 160
				easing.type: Easing.OutQuad
			}
		}
	}

	ParallelAnimation
	{
		id: enter_anim
		running: false

		PropertyAnimation
		{
			target: notif_card
			property: "opacity"
			to: 1
			duration: 160
			easing.type: Easing.OutQuad
		}

		PropertyAnimation
		{
			target: notif_card
			property: "y"
			to: 0
			duration: 160
			easing.type: Easing.OutQuad
		}
	}

	Timer
	{
		id: hide_timer
		interval: defaultTimeout
		repeat: false
		onTriggered: _showNext()
	}

	IpcHandler
	{
		target: "notif"

		function show_notification(
			id: int,
			replaces_id: int,
			app_name: string,
			app_icon: string,
			summary: string,
			body: string,
			urgency: int,
			image: string,
			expire_timeout: int
		) 
		{
			notif._enqueueNotification({
				id: id,
				replaces_id: replaces_id,
				app_name: app_name ?? "",
				app_icon: app_icon ?? "",
				summary: summary ?? "",
				body: body ?? "",
				urgency: urgency ?? 0,
				image: image ?? "",
				actions: [],
				hints: ({}),
				expire_timeout: expire_timeout
			})
		}
	}

	function _resetContent() {
		notifId = 0
		replacesId = 0
		appName = ""
		appIcon = ""
		summary = ""
		body = ""
		urgency = 0
		image = ""
		expireTimeout = -1
	}

	function _resolveTimeout(timeoutValue) {
		if (timeoutValue === 0) {
			return 0
		}
		if (timeoutValue < 0 || timeoutValue === undefined || timeoutValue === null) {
			return 0
		}
		return timeoutValue
	}

	function _applyNotification(n) {
		notifId = n.id
		replacesId = n.replaces_id
		appName = n.app_name
		appIcon = n.app_icon
		summary = n.summary
		body = n.body
		urgency = n.urgency
		image = n.image
		expireTimeout = n.expire_timeout

		showing = true

		const timeout = _resolveTimeout(expireTimeout)
		if (timeout > 0) {
			hide_timer.interval = timeout
			hide_timer.restart()
		} else {
			hide_timer.stop()
		}
	}

	property var pendingNotification: null

	function _transitionTo(n) {
		pendingNotification = n
		swap_anim.restart()
	}

	function _showNext() {
		if (queue.length === 0) {
			showing = false
			_resetContent()
			return
		}
		if (!showing) {
			_applyNotification(queue.shift())
			notif_card.opacity = 0
			notif_card.y = 8
			enter_anim.restart()
			return
		}
		_transitionTo(queue.shift())
	}

	function _enqueueNotification(n) {
		queue.push(n)
		if (!showing) {
			_showNext()
		}
	}
}
