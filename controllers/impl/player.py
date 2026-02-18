import subprocess
from typing import Literal
from lib.rofi import RofiShell
import time

# TODO fix this up, its so messy.

no_players_mesg = "No players found"
playing_mesg = "Playing"

main_rasi = "~/.config/rofi/player/main.rasi"
display_rasi = "~/.config/rofi/player/display.rasi"


class PlayerController:

    def __init__(self) -> None:
        self.rofi = RofiShell(main_rasi)
        self.current_title: str = ""


    def launch(self):

        while True:
        
            self.status = self.is_update_needed()

            if self.status == "NoPlayers":
                self.trigger_display(" ", "No Players Found.")

            elif self.status == "NoUpdates":
                pass

            elif self.status == "Updates":
                self.get_info()
                self.trigger_main(self.name, self.options)

            # listen for rofi if it returned

            try:
                selected = self.rofi.wait(0.5)
                if selected is None: continue
            except subprocess.TimeoutExpired:
                continue
            
            print("Selected: ", selected)
            
            if selected == "": # dispaly rofi will always return "" so it won't go past here
                exit()

            # this only executes if rofi has ended, the script should also end after this

            self.exec(selected)
            self.trigger_main(self.name, self.options)



    def is_update_needed(self) -> Literal["NoPlayers", "NoUpdates", "Updates"]:

        title = RofiShell.Run("playerctl metadata xesam:title")

        # only update the rofi process if player starts/stops or title changes

        if title == no_players_mesg:
            if self.current_title == "":
                return "NoUpdates"
            
            self.current_title = ""
            return "NoPlayers"
        
        if title == self.current_title:
            return "NoUpdates"
        
        self.current_title = title
        return "Updates"


    def get_info(self):

        self.title = RofiShell.Run("playerctl metadata xesam:title")
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
        

    def exec(self, seleted: str):
        
        if seleted == self.options[0]:
            RofiShell.Run("playerctl play-pause")
            self.get_info()
        elif seleted == self.options[1]:
            RofiShell.Run("playerctl next")
            while self.is_update_needed() != "Updates":
                continue
            self.get_info()
        elif seleted == self.options[2]:
            RofiShell.Run("playerctl previous")
            while self.is_update_needed() != "Updates":
                continue
            self.get_info()
        elif seleted == self.options[3]:
            RofiShell.Run("playerctl stop")
        


    
    def trigger_main(self, prompt: str, options: list[str]):

        self.rofi.updateTheme(main_rasi)

        self.rofi.display(
            mode= RofiShell.Mode.dmenu,
            prompt=prompt,
            options=options
        )

    def trigger_display(self, prompt: str, mesg: str):

        self.rofi.updateTheme(display_rasi)

        self.rofi.display(
            mode= RofiShell.Mode.dmenu,
            prompt=prompt,
            mesg=mesg,
        )


if __name__ == "__main__":
	c = PlayerController()
	c.launch()   