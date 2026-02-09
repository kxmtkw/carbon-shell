#!/bin/sh

pkill rofi # a bit brute force but meh

echo $CARBONPY

if [[ -z $1 ]]; then
    set -- "--list"
fi

case $1 in
	"--list")
		echo Supporter controllers:
		echo launcher windows power battery screenshot wifi run
	;;
	"launcher")
		rofi -show drun -theme ~/.config/rofi/launcher.rasi 
	;;
	"windows")
		rofi -show window -theme ~/.config/rofi/windows.rasi
	;;
	"power")
		$CARBONPY ~/.carbon/controllers/impl/power.py
	;;
	"battery") 
		$CARBONPY ~/.carbon/controllers/impl/battery.py
	;;
	"screenshot") 
		$CARBONPY ~/.carbon/controllers/impl/screenshot.py
	;;
	"wifi") 
		$CARBONPY ~/.carbon/controllers/impl/wifi.py
	;;
	"run") 
		$CARBONPY ~/.carbon/controllers/impl/run.py
	;;
	*)
		notify-send "Unknown controller!" $1
	;;
esac