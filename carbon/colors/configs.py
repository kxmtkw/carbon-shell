
def update_kitty(s: dict[str, str]):

    base = (
        "// NOTE: written by carbon shell\n" 
        f"selection_foreground     {s["on_surface"]}\n"
        f"selection_background     {s["surface_container_highest"]}\n"
        f"active_border_color      {s["on_surface"]}\n"
        f"inactive_border_color    {s["on_surface"]}\n"
        f"active_tab_foreground    {s["on_surface"]}\n"
        f"active_tab_background    {s["surface_container"]}\n"
        f"inactive_tab_foreground  {s["on_surface"]}\n"
        f"inactive_tab_background  {s["background"]}\n"
        f"background               {s["background"]}\n"
        f"foreground               {s["on_surface"]}\n"
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
        f"cursor                   {s["on_surface"]}\n"
        f"cursor_text_color        {s["on_surface"]}\n"
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
    base = (
        "// NOTE: written by carbon shell\n"
        "* {\n"
        f"background:                     {s["background"]};\n"
        f"surfaceContainer:               {s["surface_container"]};\n"
        f"onSurface:                      {s["on_surface"]};\n"
        f"surfaceContainerHigh:           {s["surface_container_high"]};\n"
        f"surfaceContainerHighest:        {s["surface_container_highest"]};\n"
        f"outline:                        {s["outline"]};\n"
        f"primary:                        {s["primary"]};\n"
        f"onPrimary:                      {s["on_primary"]};\n"
        "}"
    )

    return base


def update_quickshell(s: dict[str, str]) -> str:
    base = """
    // NOTE: written by carbon shell
    pragma Singleton

    import QtQuick
    import Quickshell

    Singleton 
    {
    property color invisible					 : "#00000000"\n
    """

    for name, val in s.items():
        base += f"property color {name:<30}: \"{val}\"\n"

    base += "\n}"

    return base

   
