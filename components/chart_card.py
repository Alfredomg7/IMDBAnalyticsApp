import dash_mantine_components as dmc
from dash import dcc
from config import PRIMARY_COLOR
from components.empty_chart import create_empty_chart

def create_chart_card(title: str, chart_id: str, height: int, border_color: str) -> dmc.Paper:
    """
    Create a plotly chart wrapped in a styled card component with loading indicator.
    
    Args:
        title (str): Title to display on the card
        chart_id (str): ID for the dcc.Graph component
        height (int): Height of the chart in pixels
        border_color (str): Color for the top border of the card
        
    Returns:
        dmc.Paper: A Paper component containing the chart card with loading
    """
    return dmc.Paper([
        dmc.Title(title, order=3, mb=15, c="gray.8"),
        dmc.Box(
            children=[
                dmc.LoadingOverlay(
                    visible=True,  # Start with loading visible
                    id=f"{chart_id}-loading",
                    variant="dots",
                    loaderProps={"color": PRIMARY_COLOR, "size": "xl"},
                    overlayProps={"radius": "md", "blur": 2, "opacity": 0.7},
                    zIndex=10,
                ),
                dcc.Graph(id=chart_id,
                        style={"height": height},
                        figure=create_empty_chart("Loading data...")
                )
            ],
            pos="relative"
        )
    ], 
    p=20, 
    withBorder=True, 
    radius="md", 
    style={"border": f"3px solid {border_color}"}
    )
