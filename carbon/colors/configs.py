

def update_alacritty(s: dict[str, str]):

	base = f"""
# NOTE: written by carbon shell
[colors]
[colors.primary]
foreground = "{s['onSurface']}"
background = "{s['background']}"

[colors.normal]
red     = "#fdb2d4"
yellow  = "#f8e9a6"
green   = "#cdf6a0"
cyan    = "#aaeaf6"
blue    = "#98c4f3"
magenta = "#c4a9f8"

[colors.bright]
red     = "#fdb2d4"
yellow  = "#f8e9a6"
green   = "#cdf6a0"
cyan    = "#aaeaf6"
blue    = "#98c4f3"
magenta = "#c4a9f8"
"""

	return base


def update_kitty(s: dict[str, str]):

	base = (
		"// NOTE: written by carbon shell\n" 
		f"selection_foreground     {s["onSurface"]}\n"
		f"selection_background     {s["surfaceContainerHighest"]}\n"
		f"active_border_color      {s["onSurface"]}\n"
		f"inactive_border_color    {s["onSurface"]}\n"
		f"active_tab_foreground    {s["onSurface"]}\n"
		f"active_tab_background    {s["surfaceContainer"]}\n"
		f"inactive_tab_foreground  {s["onSurface"]}\n"
		f"inactive_tab_background  {s["background"]}\n"
		f"background               {s["background"]}\n"
		f"foreground               {s["onSurface"]}\n"
		f"color0                   #323234\n"
		f"color1                   #b3261e\n"
		f"color2                   #1b6b44\n"
		f"color3                   #7f5700\n"
		f"color4                   #005ac1\n"
		f"color5                   #7b1fa2\n"
		f"color6                   #006a6a\n"
		f"color7                   #e6e1e5\n"
		f"color8                   #49454f\n"
		f"color9                   #ff5449\n"
		f"color10                  #4fd8a0\n"
		f"color11                  #ffb74d\n"
		f"color12                  #6f9cff\n"
		f"color13                  #ce93d8\n"
		f"color14                  #4dd0e1\n"
		f"color15                  #ffffff\n"
		f"cursor                   {s["onSurface"]}\n"
		f"cursor_text_color        {s["onSurface"]}\n"
		f"url_color                {s["tertiary"]}\n"
	)

	return base


def update_hypr(s: dict[str, str]):
	outline = s["outline"][1:]

	base = (
		"# NOTE: written by carbon shell\n"
		f"$border_active = rgb({outline})\n"
		f"$border_inactive = rgba({outline}40)\n"
	)

	return base


def update_rofi(s: dict[str, str]):
	base = theme_str = f"""
// NOTE: written by carbon shell
* {'{'}
"""
	for name, val in s.items():
		base += f"{name:<30}: {val};\n"

	base += "\n}"

	return base



def update_quickshell(s: dict[str, str]) -> str:
	base = """
// NOTE: written by carbon shell
pragma Singleton

import QtQuick
import Quickshell

Singleton 
{
	property color _invisible					 : "#00000000"\n
"""

	for name, val in s.items():
		base += f"  property color _{name:<30}: \"{val}\"\n"

	base += "\n}"

	return base

   
