
def updateHypr(s: dict[str, str]) -> str:
    outline = s["surfaceVariant"][1:]
    
    return f"""# NOTE: written by carbon shell
$border_active = rgb({outline})
$border_inactive = rgba({outline}40)
$background = rgb({s['background'][1:]})
$surface = rgb({s['surface'][1:]})
$onSurface = rgb({s['onSurface'][1:]})
$surfaceContainer = rgb({s['surfaceContainer'][1:]})
$primary = rgb({s['primary'][1:]})
$onPrimary = rgb({s['onPrimary'][1:]})
$primaryContainer = rgb({s['primaryContainer'][1:]})
$secondary = rgb({s['secondary'][1:]})
$onSecondary = rgb({s['onSecondary'][1:]})
$secondaryContainer = rgb({s['secondaryContainer'][1:]})
$tertiary = rgb({s['tertiary'][1:]})
$onTertiary = rgb({s['onTertiary'][1:]})
$tertiaryContainer = rgb({s['tertiaryContainer'][1:]})
$error = rgb({s['error'][1:]})
$errorContainer = rgb({s['errorContainer'][1:]})
$onErrorContainer = rgb({s['onErrorContainer'][1:]})
"""
