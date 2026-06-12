

def get_rigid_style() -> str:
	return f"""
// NOTE: written by carbon shell
* {{
	styleOuterBorderRadius: 2px;

    styleInnerBorderWidth: 2px;
	styleInnerBorderRadius: 2px;
	styleInnerBorderColor: @surfaceContainer;

	styleWidgetBorderRadius: 2px;
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