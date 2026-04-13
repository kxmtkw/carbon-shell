def updateKitty(s: dict[str, str]) -> str:
    return f"""\
// NOTE: written by carbon shell
selection_foreground     {s['onSurface']}
selection_background     {s['surfaceContainerHighest']}
active_border_color      {s['onSurface']}
inactive_border_color    {s['onSurface']}
active_tab_foreground    {s['onSurface']}
active_tab_background    {s['surfaceContainer']}
inactive_tab_foreground  {s['onSurface']}
inactive_tab_background  {s['background']}
background               {s['background']}
foreground               {s['onSurface']}
color0                   {s['black']}
color1                   {s['red']}
color2                   {s['green']}
color3                   {s['yellow']}
color4                   {s['blue']}
color5                   {s['magenta']}
color6                   {s['cyan']}
color7                   {s['white']}
color8                   {s['black']}
color9                   {s['red']}
color10                  {s['green']}
color11                  {s['yellow']}
color12                  {s['blue']}
color13                  {s['magenta']}
color14                  {s['cyan']}
color15                  {s['white']}
cursor                   {s['onSurface']}
cursor_text_color        {s['onSurface']}
url_color                {s['tertiary']}
"""