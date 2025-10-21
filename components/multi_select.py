from dash import html
import dash_mantine_components as dmc

def create_multi_select(id: str, values: list[str], title: str, color: str) -> html.Div:
    return html.Div(
        [
            dmc.Text(title, size="sm", fw=500, mb=10, mt=20),
            dmc.MultiSelect(
                id=id,
                data=[{"value": item, "label": item} for item in values],
                value=values,  # Default to all selected
                searchable=True,
                clearable=True,
                styles={"pill": {"backgroundColor": color}}
            )
        ]
    )