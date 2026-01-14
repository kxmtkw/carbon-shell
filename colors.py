import material_color_utilities as material
from PIL import Image

theme = material.theme_from_color("#00E1FF")
s = theme.schemes.dark

s = [
    ("background", s.background),
    ("surface", s.surface),
    ("surface_dim", s.surface_dim),
    ("surface_bright", s.surface_bright),
    ("surface_container_lowest", s.surface_container_lowest),
    ("surface_container_low", s.surface_container_low),
    ("surface_container", s.surface_container),
    ("surface_container_high", s.surface_container_high),
    ("surface_container_highest", s.surface_container_highest),
    ("on_surface", s.on_surface),
    ("surface_variant", s.surface_variant),
    ("on_surface_variant", s.on_surface_variant),
    ("inverse_surface", s.inverse_surface),
    ("inverse_on_surface", s.inverse_on_surface),
    ("outline", s.outline),
    ("outline_variant", s.outline_variant),
    ("shadow", s.shadow),
    ("scrim", s.scrim),
    ("surface_tint", s.surface_tint),

    ("primary", s.primary),
    ("on_primary", s.on_primary),
    ("primary_container", s.primary_container),
    ("on_primary_container", s.on_primary_container),
    ("inverse_primary", s.inverse_primary),

    ("secondary", s.secondary),
    ("on_secondary", s.on_secondary),
    ("secondary_container", s.secondary_container),
    ("on_secondary_container", s.on_secondary_container),

    ("tertiary", s.tertiary),
    ("on_tertiary", s.on_tertiary),
    ("tertiary_container", s.tertiary_container),
    ("on_tertiary_container", s.on_tertiary_container),

    ("error", s.error),
    ("on_error", s.on_error),
    ("error_container", s.error_container),
    ("on_error_container", s.on_error_container),

    ("primary_fixed", s.primary_fixed),
    ("primary_fixed_dim", s.primary_fixed_dim),
    ("on_primary_fixed", s.on_primary_fixed),
    ("on_primary_fixed_variant", s.on_primary_fixed_variant),

    ("secondary_fixed", s.secondary_fixed),
    ("secondary_fixed_dim", s.secondary_fixed_dim),
    ("on_secondary_fixed", s.on_secondary_fixed),
    ("on_secondary_fixed_variant", s.on_secondary_fixed_variant),

    ("tertiary_fixed", s.tertiary_fixed),
    ("tertiary_fixed_dim", s.tertiary_fixed_dim),
    ("on_tertiary_fixed", s.on_tertiary_fixed),
    ("on_tertiary_fixed_variant", s.on_tertiary_fixed_variant),
]


base = """
pragma Singleton

import QtQuick
import Quickshell

Singleton 
{

"""

for name, val in s:
	base += f"	property color {name:<30}: \"{val}\"\n"

base += "\n}"

with open("Config/quickshell/material/Color.qml", "w") as file:
	file.write(base)