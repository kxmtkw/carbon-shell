// shell.qml
import Quickshell
import QtQuick

import qs.panel
import qs.notifications

ShellRoot
{
    Panel
    {
        id: panel
    }

    Notification
    {
        panelWindow: panel
    }
}
