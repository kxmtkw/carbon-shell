pkill rofi # a bit brute force but meh

case $1 in
	"--list")
		echo launcher_apps launcher_run launcher_files windows power battery screenshot
	;;
	"launcher_apps")
		rofi -show drun -theme ~/.config/rofi/launcher.rasi
	;;
	"launcher_run")
		rofi -show run -theme ~/.config/rofi/launcher.rasi
	;;
	"launcher_files")
		rofi -show filebrowser -theme ~/.config/rofi/launcher.rasi
	;;
	"windows")
		rofi -show window -theme ~/.config/rofi/windows.rasi
	;;
	"power")
		python3 ~/.carbon/controllers/impl/power.py
	;;
	"battery") 
		python3 ~/.carbon/controllers/impl/battery.py
	;;
	"screenshot") 
		python3 ~/.carbon/controllers/impl/screenshot.py
	;;
	"wifi") 
		python3 ~/.carbon/controllers/impl/wifi.py
	;;
	*)
		notify-send "Unknown controller!" $1
	;;
esac