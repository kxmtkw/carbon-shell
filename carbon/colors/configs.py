
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
BackgroundAlternate={s["primaryContainer"]}
BackgroundNormal={s["surfaceContainer"]}
DecorationFocus={s["primary"]}
DecorationHover={s["primary"]}
ForegroundActive={s["primary"]}
ForegroundInactive={s["onSurface"]}
ForegroundLink={s["tertiary"]}
ForegroundNegative={s["secondary"]}
ForegroundNeutral={s["onSurface"]}
ForegroundNormal={s["onSurface"]}
ForegroundPositive={s["primary"]}
ForegroundVisited={s["tertiary"]}

[Colors:Selection]
BackgroundAlternate={s["surfaceContainerHigh"]}
BackgroundNormal={s["surfaceContainerHigh"]}
DecorationFocus={s["primary"]}
DecorationHover={s["primary"]}
ForegroundActive={s["primary"]}
ForegroundInactive={s["onSurface"]}
ForegroundLink={s["tertiary"]}
ForegroundNegative={s["secondary"]}
ForegroundNeutral={s["onSurface"]}
ForegroundNormal={s["onSurface"]}
ForegroundPositive={s["primary"]}
ForegroundVisited={s["tertiary"]}

[Colors:Tooltip]
BackgroundAlternate={s["surfaceContainer"]}
BackgroundNormal={s["background"]}
DecorationFocus={s["primary"]}
DecorationHover={s["primary"]}
ForegroundActive={s["primary"]}
ForegroundInactive={s["onSurface"]}
ForegroundLink={s["tertiary"]}
ForegroundNegative={s["secondary"]}
ForegroundNeutral={s["onSurface"]}
ForegroundNormal={s["onSurface"]}
ForegroundPositive={s["primary"]}
ForegroundVisited={s["tertiary"]}

[Colors:View]
BackgroundAlternate={s["surfaceContainer"]}
BackgroundNormal={s["background"]}
DecorationFocus={s["primary"]}
DecorationHover={s["primary"]}
ForegroundActive={s["primary"]}
ForegroundInactive={s["onSurface"]}
ForegroundLink={s["tertiary"]}
ForegroundNegative={s["secondary"]}
ForegroundNeutral={s["onSurface"]}
ForegroundNormal={s["onSurface"]}
ForegroundPositive={s["primary"]}
ForegroundVisited={s["tertiary"]}

[Colors:Window]
BackgroundAlternate={s["surfaceContainer"]}
BackgroundNormal={s["background"]}
DecorationFocus={s["primary"]}
DecorationHover={s["primary"]}
ForegroundActive={s["primary"]}
ForegroundInactive={s["onSurface"]}
ForegroundLink={s["tertiary"]}
ForegroundNegative={s["secondary"]}
ForegroundNeutral={s["onSurface"]}
ForegroundNormal={s["onSurface"]}
ForegroundPositive={s["primary"]}
ForegroundVisited={s["tertiary"]}

[General]
Name=Carbon
shadeSortColumn=true

[KDE]
contrast=10
"""

	return base


def update_alacritty(s: dict[str, str]):

	base = f"""
# NOTE: written by carbon shell
[colors]
[colors.primary]
foreground = "{s['onSurface']}"
background = "{s['surface']}"

[colors.normal]
red     = "{s['red']}"
yellow  = "{s['yellow']}"
green   = "{s['green']}"
cyan    = "{s['cyan']}"
blue    = "{s['blue']}"
magenta = "{s['magenta']}"
white   = "{s['white']}"
black   = "{s['black']}"

[colors.bright]
red     = "{s['red']}"
yellow  = "{s['yellow']}"
green   = "{s['green']}"
cyan    = "{s['cyan']}"
blue    = "{s['blue']}"
magenta = "{s['magenta']}"
white   = "{s['white']}"
black   = "{s['black']}"
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
		f"color0                   {s['black']}\n"
		f"color1                   {s['red']}\n"
		f"color2                   {s['green']}\n"
		f"color3                   {s['yellow']}\n"
		f"color4                   {s['blue']}\n"
		f"color5                   {s['magenta']}\n"
		f"color6                   {s['cyan']}\n"
		f"color7                   {s['white']}\n"
		f"color8                   {s['black']}\n"
		f"color9                   {s['red']}\n"
		f"color10                  {s['green']}\n"
		f"color11                  {s['yellow']}\n"
		f"color12                  {s['blue']}\n"
		f"color13                  {s['magenta']}\n"
		f"color14                  {s['cyan']}\n"
		f"color15                  {s['white']}\n"
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


def update_dunst(s: dict[str, str]):

	base = f"""
# NOTE: written by carbon shell
[urgency_low]
background = "{s['surfaceContainer']}"
foreground = "{s['onSurface']}"
frame_color = "{s['surfaceContainer']}"

[urgency_normal]
background = "{s['surfaceContainer']}"
foreground = "{s['onSurface']}"
frame_color = "{s['secondary']}"

[urgency_critical]
background = "{s['surfaceContainer']}"
foreground = "{s['onSurface']}"
frame_color = "{s['primary']}"
"""
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

   
