from dash import html, dcc
import dash_mantine_components as dmc

def create_range_slider(id: str, min_value: int, max_value: int, title: str, step: int = 1, mark_step: int = None) -> html.Div:
    """
    Create a range slider component using dcc.RangeSlider
    
    Args:
        id: Component ID
        min_value: Minimum value
        max_value: Maximum value
        title: Title text
        step: Step size for slider (default: 1)
        mark_step: Step size for marks (default: None, auto-calculated)
    """
    if mark_step is None:
        range_size = max_value - min_value
        mark_step = range_size // 10 or 1  # At most 10 marks
    
    marks = {i: f"{i}" for i in range(min_value, max_value + 1, mark_step)}
    
    return html.Div(
        [
            dmc.Text(title, size="sm", fw=500, mb=10, mt=20),
            dcc.RangeSlider(
                id=id,
                min=min_value,
                max=max_value,
                step=step,
                value=[min_value, max_value],
                marks=marks,
                tooltip={
                    "placement": "bottom",
                    "always_visible": True
                }
            )
        ],
    )