
def update_kde(s: dict[str, str]) -> str:
    return f"""
[ColorEffects:Disabled]
Color = {s["surfaceVariant"]}
ColorAmount = 0
ColorEffect = 0
ContrastAmount = 0.65
ContrastEffect = 1
IntensityAmount = 0.1
IntensityEffect = 2

[ColorEffects:Inactive]
ChangeSelectionColor = true
Color = {s["outlineVariant"]}
ColorAmount = 0.025
ColorEffect = 2
ContrastAmount = 0.1
ContrastEffect = 2
Enable = false
IntensityAmount = 0
IntensityEffect = 0

[Colors:Button]
BackgroundAlternate = {s["surfaceContainerHigh"]}
BackgroundNormal = {s["surfaceContainer"]}
DecorationFocus = {s["primary"]}
DecorationHover = {s["primary"]}
ForegroundActive = {s["primary"]}
ForegroundInactive = {s["onSurfaceVariant"]}
ForegroundLink = {s["blue"]}
ForegroundNegative = {s["error"]}
ForegroundNeutral = {s["orange"]}
ForegroundNormal = {s["onSurface"]}
ForegroundPositive = {s["green"]}
ForegroundVisited = {s["outline"]}

[Colors:Selection]
BackgroundAlternate = {s["primaryContainer"]}
BackgroundNormal = {s["primary"]}
DecorationFocus = {s["primary"]}
DecorationHover = {s["primary"]}
ForegroundActive = {s["onPrimaryContainer"]}
ForegroundInactive = {s["onSurface"]}
ForegroundLink = {s["yellow"]}
ForegroundNegative = {s["error"]}
ForegroundNeutral = {s["orange"]}
ForegroundNormal = {s["onPrimary"]}
ForegroundPositive = {s["green"]}
ForegroundVisited = {s["onSurfaceVariant"]}

[Colors:Tooltip]
BackgroundAlternate = {s["surfaceContainerHigh"]}
BackgroundNormal = {s["surfaceContainer"]}
DecorationFocus = {s["primary"]}
DecorationHover = {s["primary"]}
ForegroundActive = {s["primary"]}
ForegroundInactive = {s["onSurfaceVariant"]}
ForegroundLink = {s["blue"]}
ForegroundNegative = {s["error"]}
ForegroundNeutral = {s["orange"]}
ForegroundNormal = {s["onSurface"]}
ForegroundPositive = {s["green"]}
ForegroundVisited = {s["outline"]}

[Colors:View]
BackgroundAlternate = {s["surfaceContainerHigh"]}
BackgroundNormal = {s["surfaceContainer"]}
DecorationFocus = {s["primary"]}
DecorationHover = {s["primary"]}
ForegroundActive = {s["primary"]}
ForegroundInactive = {s["onSurfaceVariant"]}
ForegroundLink = {s["blue"]}
ForegroundNegative = {s["error"]}
ForegroundNeutral = {s["orange"]}
ForegroundNormal = {s["onSurface"]}
ForegroundPositive = {s["green"]}
ForegroundVisited = {s["outline"]}

[Colors:Window]
BackgroundAlternate = {s["surfaceContainerHigh"]}
BackgroundNormal = {s["surfaceContainer"]}
DecorationFocus = {s["primary"]}
DecorationHover = {s["primary"]}
ForegroundActive = {s["primary"]}
ForegroundInactive = {s["onSurfaceVariant"]}
ForegroundLink = {s["blue"]}
ForegroundNegative = {s["error"]}
ForegroundNeutral = {s["orange"]}
ForegroundNormal = {s["onSurface"]}
ForegroundPositive = {s["green"]}
ForegroundVisited = {s["outline"]}

[Colors:Complementary]
BackgroundAlternate = {s["surfaceContainerHighest"]}
BackgroundNormal = {s["surfaceContainer"]}
DecorationFocus = {s["primaryFixed"]}
DecorationHover = {s["primary"]}
ForegroundActive = {s["orange"]}
ForegroundInactive = {s["outline"]}
ForegroundLink = {s["primary"]}
ForegroundNegative = {s["red"]}
ForegroundNeutral = {s["yellow"]}
ForegroundNormal = {s["onSurface"]}
ForegroundPositive = {s["green"]}
ForegroundVisited = {s["primary"]}

[General]
ColorScheme= Carbon
Name= Carbon
shadeSortColumn = true

[KDE]
contrast = 4

[WM]
activeBackground = {s["surfaceContainer"]}
activeBlend = {s["white"]}
activeForeground = {s["onSurface"]}
inactiveBackground = {s["surfaceContainer"]}
inactiveBlend = {s["surfaceContainerHighest"]}
inactiveForeground = {s["outline"]}
"""
