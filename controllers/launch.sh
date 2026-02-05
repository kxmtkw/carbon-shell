pkill rofi # a bit brute force but meh

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
	"run") 
		python3 ~/.carbon/controllers/impl/run.py
	;;
	*)
		notify-send "Unknown controller!" $1
	;;
esac