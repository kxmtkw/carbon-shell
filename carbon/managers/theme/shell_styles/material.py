

def get_material_style() -> str:
	return f"""
// NOTE: written by carbon shell
* {{
	styleOuterBorderRadius: 20px;

    styleInnerBorderWidth: 0px;
	styleInnerBorderRadius: 12px;
	styleInnerBorderColor: @surfaceContainer;

	styleWidgetBorderRadius: 8px;
	styleWidgetSpace: 12px;

	styleOuterMargins: 10px;
	styleInnerMargins: 10px;
	styleInnerPadding: 20px;
	
	styleMainBoxColor: @background;

	styleSelectionBar: 0px 0px 0px 8px;
	styleSelectionColor: @primaryContainer;
	styleActiveColor: @surfaceContainerHigh;
	styleActiveSelectionColor: @primary;
}}
"""