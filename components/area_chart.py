from typing import Any
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
from config import PRIMARY_COLOR, COLOR_DISCRETE_SEQUENCE
from utils.chart_styles import apply_common_styles, format_hover_template

def create_area_chart(
    df: pl.DataFrame,
    x_col: str,
    y_col: str,
    title: str = "",
    color_col: str = None,
    color_sequence: list = None,
    hover_name: str = None,
    hover_data: list = None,
    line_width: int = 2,
    stacked: bool = True
) -> go.Figure:
    """
    Create a plotly area chart styled component.
    
    Args:
        df: DataFrame with data
        x_col (str): Column name for x-axis
        y_col (str): Column name for y-axis
        title (str): Chart title
        color_col (str): Column name for color grouping
        color_sequence (list): Custom color sequence for discrete colors
        hover_name (str): Column name for hover label (sets hovertext)
        hover_data (list): Additional columns to show in hover tooltip
        line_width (int): Width of the lines
        stacked (bool): Whether to stack areas (default: True)

    Returns:
        go.Figure: Configured area chart
    """
    hover_name = hover_name if hover_name else x_col
    hover_data = hover_data if hover_data else [y_col]
    hovertemplate, custom_data_cols = format_hover_template(hover_name, hover_data)

    base_args: dict[str, Any] = dict(data_frame=df, x=x_col, y=y_col, title=title)
    if custom_data_cols:
        base_args['custom_data'] = custom_data_cols
    if color_col:
        chart_colors = color_sequence or COLOR_DISCRETE_SEQUENCE
        base_args['color'] = color_col
        base_args['color_discrete_sequence'] = chart_colors
    
    fig = px.area(**base_args)
    
    # Set area color and line for single area charts
    if not color_col:
        fig.update_traces(
            fillcolor=PRIMARY_COLOR,
            line_color=PRIMARY_COLOR
        )

    
    # Implement custom styling
    fig.update_traces(
        line_width=line_width,
        hovertemplate=hovertemplate
    )
    
    if not stacked and color_col:
        fig.update_traces(stackgroup=None)
    
    fig = apply_common_styles(fig, title, x_col, y_col)

    return fig
