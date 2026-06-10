

def get_material_style() -> str:
	return f"""
// NOTE: written by carbon shell
* {{
    styleInlineBorderWidth: 0px;
	styleOuterBorderRadius: 20px;
	styleInnerBorderRadius: 12px;
	styleWidgetBorderRadius: 8px;

	styleGaps: 10px;
	styleInnerGaps: 20px;
	styleWidgetSpace: 12px;

	styleInlineBorderColor: @surfaceContainerHighest;
	styleBoxColor: @background;

	styleSelectionBar: 0px 0px 0px 8px;
	styleSelectionColor: @primaryContainer;
	styleActiveColor: @surfaceContainerHigh;
	styleActiveSelectionColor: @primary;
}}
"""