from rofi import RofiShell
import time

no_players_mesg = "No players found"
playing_mesg = "Playing"


main_rasi = "~/.config/rofi/player/main.rasi"
display_rasi = "~/.config/rofi/player/display.rasi"

class PlayerController:

    def __init__(self) -> None:
        self.rofi = RofiShell(main_rasi)


    def get_info(self):

        self.title = RofiShell.Run("playerctl metadata xesam:title")

        if self.title == no_players_mesg:
            self.trigger_display(" ", "No Players Found")
            exit()

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


    def launch(self):
        
        self.get_info()

        selected = self.rofi.display(
            self.name,
            "",
            self.options
        )

        if not selected:
            exit()
        
        self.exec(selected)
        

    def exec(self, seleted: str):
        
        if seleted == self.options[0]:
            RofiShell.Run("playerctl play-pause")
        elif seleted == self.options[1]:
            RofiShell.Run("playerctl next")
        elif seleted == self.options[2]:
            RofiShell.Run("playerctl previous")
        elif seleted == self.options[3]:
            RofiShell.Run("playerctl stop")

    
    def trigger_display(self, prompt: str, mesg: str):

        self.rofi.updateTheme(display_rasi)

        self.rofi.display(
            prompt,
            mesg,
            []
        )


if __name__ == "__main__":
	c = PlayerController()
	c.launch()   