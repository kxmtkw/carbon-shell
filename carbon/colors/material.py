
import material_color_utilities as material
from PIL import Image
from pathlib import Path

from carbon.helpers import CarbonError

class MaterialColors:


    class Variant:
        ash      = (0.1, material.Variant.VIBRANT)
        coal     = (0.2, material.Variant.MONOCHROME)
        graphite = (0.2, material.Variant.TONALSPOT)
        diamond  = (0.6, material.Variant.VIBRANT)


    def __init__(self):
        self.darkScheme: material.DynamicScheme 
        self.lightScheme: material.DynamicScheme

        self.darkMapping: dict[str, str]
        self.lightMapping: dict[str, str]

        self._contrast: float = 0
        self._variant = 0


    def generate_from_image(self, image: str, variant: tuple):

        if not Path(image).exists():
            CarbonError(f"Image not found: {image}").halt()

        theme = material.theme_from_image(Image.open(image), variant[0], variant[1])

        self.darkScheme = theme.schemes.dark
        self.lightScheme = theme.schemes.light

        self.darkMapping = self.make_mapping(self.darkScheme)
        self.lightMapping = self.make_mapping(self.lightScheme)


    def generate_from_color(self, color: str, variant: tuple):

        theme = material.theme_from_color(color, variant[0], variant[1])

        self.darkScheme = theme.schemes.dark
        self.lightScheme = theme.schemes.light

        self.darkMapping = self.make_mapping(self.darkScheme)
        self.lightMapping = self.make_mapping(self.lightScheme)


    def make_mapping(self, s: material.DynamicScheme) -> dict[str, str]:
        scheme = {
            "background": s.background,
            "backgroundTransparentxAA": f"{s.background}40",
            "backgroundTransparentAAx": f"#40{s.background.removeprefix('#')}",
            "surface": s.surface,
            "surfaceDim": s.surface_dim,
            "surfaceBright": s.surface_bright,
            "surfaceContainerLowest": s.surface_container_lowest,
            "surfaceContainerLow": s.surface_container_low,
            "surfaceContainer": s.surface_container,
            "surfaceContainerHigh": s.surface_container_high,
            "surfaceContainerHighest": s.surface_container_highest,
            "onSurface": s.on_surface,
            "surfaceVariant": s.surface_variant,
            "onSurfaceVariant": s.on_surface_variant,
            "inverseSurface": s.inverse_surface,
            "inverseOnSurface": s.inverse_on_surface,
            "outline": s.outline,
            "outlineVariant": s.outline_variant,
            "shadow": s.shadow,
            "scrim": s.scrim,
            "surfaceTint": s.surface_tint,

            "primary": s.primary,
            "onPrimary": s.on_primary,
            "primaryContainer": s.primary_container,
            "onPrimaryContainer": s.on_primary_container,
            "inversePrimary": s.inverse_primary,

            "secondary": s.secondary,
            "onSecondary": s.on_secondary,
            "secondaryContainer": s.secondary_container,
            "onSecondaryContainer": s.on_secondary_container,

            "tertiary": s.tertiary,
            "onTertiary": s.on_tertiary,
            "tertiaryContainer": s.tertiary_container,
            "onTertiaryContainer": s.on_tertiary_container,

            "error": s.error,
            "onError": s.on_error,
            "errorContainer": s.error_container,
            "onErrorContainer": s.on_error_container,

            "primaryFixed": s.primary_fixed,
            "primaryFixedDim": s.primary_fixed_dim,
            "onPrimaryFixed": s.on_primary_fixed,
            "onPrimaryFixedVariant": s.on_primary_fixed_variant,

            "secondaryFixed": s.secondary_fixed,
            "secondaryFixedDim": s.secondary_fixed_dim,
            "onSecondaryFixed": s.on_secondary_fixed,
            "onSecondaryFixedVariant": s.on_secondary_fixed_variant,

            "tertiaryFixed": s.tertiary_fixed,
            "tertiaryFixedDim": s.tertiary_fixed_dim,
            "onTertiaryFixed": s.on_tertiary_fixed,
            "onTertiaryFixedVariant": s.on_tertiary_fixed_variant,
        }


        return scheme