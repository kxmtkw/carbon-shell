import subprocess
from typing import Literal
from rofi import RofiShell
import time

no_players_mesg = "No players found"
playing_mesg = "Playing"

main_rasi = "~/.config/rofi/player/main.rasi"
display_rasi = "~/.config/rofi/player/display.rasi"


class PlayerController:

    def __init__(self) -> None:
        self.rofi = RofiShell(main_rasi)
        self.current_title: str = None


    def launch(self):
        active_process = None 

        while True:

            status = self.get_info()
            print(status)

            if status == "NoPlayers":
                if active_process: active_process.kill(); active_process.wait()
                active_process = self.trigger_display(" ", "No Players Found.")

            elif status == "NoUpdates":
                pass

            elif status == "Updated":
                if active_process: active_process.kill(); active_process.wait()
                active_process = self.trigger_main(self.name, self.options)

            # listen for rofi if it returned

            try:
                if active_process:
                    active_process.wait(1)
                else:
                    continue
            except subprocess.TimeoutExpired:
                continue
            
            # this only executes if rofi has ended, the script should also end after this

            selected = active_process.stdout.read().strip()
            print("Selected: ", selected)

            if not selected: # dispaly rofi will always return "" so it won't go past here
                exit()
            
            self.exec(selected)
            exit()


    def get_info(self) -> Literal["NoPlayers", "NoUpdates", "Updates"]:

        self.title = RofiShell.Run("playerctl metadata xesam:title")

        # only update the rofi process if player starts/stops or title changes

        if self.title == no_players_mesg:
            if self.current_title == "":
                return "NoUpdates"
            
            self.current_title = ""
            return "NoPlayers"
        
        if self.title == self.current_title:
            return "NoUpdates"
        
        # formatting

        self.current_title = self.title

        self.artist = RofiShell.Run("playerctl metadata xesam:artist")

        if len(self.title) > 16:
            self.title = f"{self.title[:16]}..."
        
        if len(self.artist) > 16:
            self.artist = f"{self.artist[:16]}..."

        self.name = f"  {self.title} - {self.artist}"

        self.is_playing = True if RofiShell.Run("playerctl status") == playing_mesg else False

        self.options = [
            "  Pause" if self.is_playing else "  Play",
            "  Next",
            "  Previous",
            "  Stop"
        ]

        return "Updated"
        

    def exec(self, seleted: str):
        
        if seleted == self.options[0]:
            RofiShell.Run("playerctl play-pause")
        elif seleted == self.options[1]:
            RofiShell.Run("playerctl next")
        elif seleted == self.options[2]:
            RofiShell.Run("playerctl previous")
        elif seleted == self.options[3]:
            RofiShell.Run("playerctl stop")

    
    def trigger_main(self, prompt: str, options: list[str]) -> subprocess.Popen:

        self.rofi.updateTheme(main_rasi)

        return self.rofi.displayNoBlock(
            prompt,
            "",
            options
        )

    def trigger_display(self, prompt: str, mesg: str) -> subprocess.Popen:

        self.rofi.updateTheme(display_rasi)

        return self.rofi.displayNoBlock(
            prompt,
            mesg,
            []
        )


if __name__ == "__main__":
	c = PlayerController()
	c.launch()   