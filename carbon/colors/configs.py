
def update_kde(s: dict[str, str]):

	base = f"""
[ColorEffects:Disabled]
Color={s["primary"]}
ColorAmount=1
ColorEffect=1
ContrastAmount=0.75
ContrastEffect=1
IntensityAmount=0.45
IntensityEffect=0

[ColorEffects:Inactive]
ChangeSelectionColor=true
Color=0,0,0
ColorAmount=1
ColorEffect=1
ContrastAmount=0.25
ContrastEffect=1
Enable=false
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate={s["surface"]}
BackgroundNormal={s["background"]}
DecorationFocus={s["primaryContainer"]}
DecorationHover={s["surfaceContainer"]}
ForegroundActive={s["onPrimary"]}
ForegroundInactive={s["onSurface"]}
ForegroundLink={s["secondaryContainer"]}
ForegroundNegative={s["secondary"]}
ForegroundNeutral={s["tertiary"]}
ForegroundNormal={s["onSurface"]}
ForegroundPositive={s["primary"]}
ForegroundVisited={s["primaryContainer"]}

[Colors:Selection]
BackgroundAlternate={s["surface"]}
BackgroundNormal={s["background"]}
DecorationFocus={s["primaryContainer"]}
DecorationHover={s["surfaceContainer"]}
ForegroundActive={s["onPrimary"]}
ForegroundInactive={s["onSurface"]}
ForegroundLink={s["secondaryContainer"]}
ForegroundNegative={s["secondary"]}
ForegroundNeutral={s["tertiary"]}
ForegroundNormal={s["onSurface"]}
ForegroundPositive={s["primary"]}
ForegroundVisited={s["primaryContainer"]}

[Colors:Tooltip]
BackgroundAlternate={s["surface"]}
BackgroundNormal={s["background"]}
DecorationFocus={s["primaryContainer"]}
DecorationHover={s["surfaceContainer"]}
ForegroundActive={s["onPrimary"]}
ForegroundInactive={s["onSurface"]}
ForegroundLink={s["secondaryContainer"]}
ForegroundNegative={s["secondary"]}
ForegroundNeutral={s["tertiary"]}
ForegroundNormal={s["onSurface"]}
ForegroundPositive={s["primary"]}
ForegroundVisited={s["primaryContainer"]}

[Colors:View]
BackgroundAlternate={s["surface"]}
BackgroundNormal={s["background"]}
DecorationFocus={s["primaryContainer"]}
DecorationHover={s["surfaceContainer"]}
ForegroundActive={s["onPrimary"]}
ForegroundInactive={s["onSurface"]}
ForegroundLink={s["secondaryContainer"]}
ForegroundNegative={s["secondary"]}
ForegroundNeutral={s["tertiary"]}
ForegroundNormal={s["onSurface"]}
ForegroundPositive={s["primary"]}
ForegroundVisited={s["primaryContainer"]}

[Colors:Window]
BackgroundAlternate={s["surface"]}
BackgroundNormal={s["background"]}
DecorationFocus={s["primaryContainer"]}
DecorationHover={s["surfaceContainer"]}
ForegroundActive={s["onPrimary"]}
ForegroundInactive={s["onSurface"]}
ForegroundLink={s["secondaryContainer"]}
ForegroundNegative={s["secondary"]}
ForegroundNeutral={s["tertiary"]}
ForegroundNormal={s["onSurface"]}
ForegroundPositive={s["primary"]}
ForegroundVisited={s["primaryContainer"]}

[General]
Name=Carbon
shadeSortColumn=true

[KDE]
contrast=10

[WM]
activeBackground=10,13,19
activeBlend=14,18,24
activeForeground=179,177,173
inactiveBackground=14,18,24
inactiveBlend=14,18,24
inactiveForeground=179,177,173
"""

	return base


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
		f"$background = rgb({s['background'][1:]})\n"
		f"$surface = rgb({s['surface'][1:]})\n"
		f"$onSurface = rgb({s['onSurface'][1:]})\n"
		f"$primary = rgb({s['primary'][1:]})\n"
		f"$onPrimary = rgb({s['onPrimary'][1:]})\n"
		f"$primaryContainer = rgb({s['primaryContainer'][1:]})\n"
		f"$error = rgb({s['error'][1:]})\n"
		f"$errorContainer = rgb({s['errorContainer'][1:]})\n"
		f"$onErrorContainer = rgb({s['onErrorContainer'][1:]})\n"
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

   
