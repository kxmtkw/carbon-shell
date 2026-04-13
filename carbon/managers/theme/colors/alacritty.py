def updateAlacritty(s: dict[str, str]) -> str:
    return f"""
# NOTE: written by carbon shell
[colors]
[colors.primary]
foreground = "{s["onSurface"]}"
background = "{s["surface"]}"

[colors.normal]
red     = "{s["red"]}"
yellow  = "{s["yellow"]}"
green   = "{s["green"]}"
cyan    = "{s["cyan"]}"
blue    = "{s["blue"]}"
magenta = "{s["magenta"]}"
white   = "{s["white"]}"
black   = "{s["black"]}"

[colors.bright]
red     = "{s["red"]}"
yellow  = "{s["yellow"]}"
green   = "{s["green"]}"
cyan    = "{s["cyan"]}"
blue    = "{s["blue"]}"
magenta = "{s["magenta"]}"
white   = "{s["white"]}"
black   = "{s["black"]}"
"""