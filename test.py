import tkinter as tk
import material_color_utilities as material
import math

theme = material.theme_from_color("#FFFFFF", 0.1)
s = theme.schemes.light

COLORS = [

    ("background",                 s.background),
    ("surface",                    s.surface),
    ("surface_dim",                s.surface_dim),
    ("surface_bright",             s.surface_bright),
    ("surface_container_lowest",   s.surface_container_lowest),
    ("surface_container_low",      s.surface_container_low),
    ("surface_container",          s.surface_container),
    ("surface_container_high",     s.surface_container_high),
    ("surface_container_highest",  s.surface_container_highest),
    ("on_surface",                 s.on_surface),
    ("surface_variant",            s.surface_variant),
    ("on_surface_variant",         s.on_surface_variant),
    ("inverse_surface",            s.inverse_surface),
    ("inverse_on_surface",         s.inverse_on_surface),
    ("outline",                    s.outline),
    ("outline_variant",            s.outline_variant),
    ("shadow",                     s.shadow),
    ("scrim",                      s.scrim),
    ("surface_tint",               s.surface_tint),


    ("primary",                    s.primary),
    ("on_primary",                 s.on_primary),
    ("primary_container",          s.primary_container),
    ("on_primary_container",       s.on_primary_container),
    ("inverse_primary",            s.inverse_primary),

    ("secondary",                  s.secondary),
    ("on_secondary",               s.on_secondary),
    ("secondary_container",        s.secondary_container),
    ("on_secondary_container",     s.on_secondary_container),

    ("tertiary",                   s.tertiary),
    ("on_tertiary",                s.on_tertiary),
    ("tertiary_container",         s.tertiary_container),
    ("on_tertiary_container",      s.on_tertiary_container),

    ("error",                      s.error),
    ("on_error",                   s.on_error),
    ("error_container",            s.error_container),
    ("on_error_container",         s.on_error_container),

    ("primary_fixed",              s.primary_fixed),
    ("primary_fixed_dim",          s.primary_fixed_dim),
    ("on_primary_fixed",           s.on_primary_fixed),
    ("on_primary_fixed_variant",   s.on_primary_fixed_variant),

    ("secondary_fixed",            s.secondary_fixed),
    ("secondary_fixed_dim",        s.secondary_fixed_dim),
    ("on_secondary_fixed",         s.on_secondary_fixed),
    ("on_secondary_fixed_variant", s.on_secondary_fixed_variant),

    ("tertiary_fixed",             s.tertiary_fixed),
    ("tertiary_fixed_dim",         s.tertiary_fixed_dim),
    ("on_tertiary_fixed",          s.on_tertiary_fixed),
    ("on_tertiary_fixed_variant",  s.on_tertiary_fixed_variant),
]


# ---- layout config ----
COLUMNS = 4          # how many color cards per row
CARD_WIDTH = 300
CARD_HEIGHT = 36
WINDOW_WIDTH = COLUMNS * CARD_WIDTH + 20

root = tk.Tk()
root.title("Material 3 – Dark Scheme")
root.geometry(f"{WINDOW_WIDTH}x600")

canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

inner = tk.Frame(canvas)
window_id = canvas.create_window((0, 0), window=inner, anchor="nw")

def sync_size(event):
	canvas.configure(scrollregion=canvas.bbox("all"))
	canvas.itemconfigure(window_id, width=canvas.winfo_width())

inner.bind("<Configure>", sync_size)
canvas.bind("<Configure>", sync_size)

# ---- build grid ----
for i, (name, color) in enumerate(COLORS):
	row = i // COLUMNS
	col = i % COLUMNS

	card = tk.Frame(
		inner,
		width=CARD_WIDTH - 10,
		height=CARD_HEIGHT,
		relief="solid",
		borderwidth=1
	)
	card.grid(row=row, column=col, padx=6, pady=6)
	card.grid_propagate(False)

	swatch = tk.Frame(card, bg=color, width=36, height=24)
	swatch.pack(side="left", padx=6)
	swatch.pack_propagate(False)

	text = tk.Frame(card)
	text.pack(side="left", fill="both", expand=True)

	tk.Label(text, text=name, anchor="w", font=("sans", 9)).pack(anchor="w")
	tk.Label(text, text=color, anchor="w", font=("monospace", 8)).pack(anchor="w")

root.mainloop()
