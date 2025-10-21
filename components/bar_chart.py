from typing import Any
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
from config import PRIMARY_COLOR, ACCENT_COLOR, COLOR_CONTINUOUS_SCALE
from utils.chart_styles import apply_common_styles, format_hover_template

def create_bar_chart(df: pl.DataFrame, x_col: str, y_col: str, title: str = "",
                    color_col: str | None = None, color_sequence: list | None = None, hover_name: str | None = None,
                    hover_data: list | None = None, horizontal: bool = False) -> go.Figure: 
    """
    Create a plotly bar chart styled component.

    Args:
        df: DataFrame with data
        x_col (str): Column name for x-axis
        y_col (str): Column name for y-axis
        title (str): Chart title
        color_col (str): Column name for color mapping
        color_sequence (list): Custom color sequence
        hover_name (str): Column name for hover label (sets hovertext)
        hover_data (list): Additional columns to show in hover tooltip
        horizontal (bool): Whether to create horizontal bars
        
    Returns:
        go.Figure: Configured bar chart
    """
    hover_name = hover_name if hover_name else (y_col if horizontal else x_col) # default to main axis label if not provided
    hover_data = hover_data if hover_data else ([x_col] if horizontal else [y_col]) # default to secondary axis label if not provided
    hovertemplate, custom_data_cols = format_hover_template(hover_name, hover_data)

    # Set orientation based on horizontal flag
    orientation = 'h' if horizontal else 'v'

    base_args: dict[str, Any] = dict(data_frame=df, x=x_col, y=y_col, title=title, orientation=orientation)
    if custom_data_cols:
        base_args['custom_data'] = custom_data_cols
    if color_col:
        chart_colors = color_sequence or COLOR_CONTINUOUS_SCALE
        base_args['color'] = color_col
        base_args['color_continuous_scale'] = chart_colors

    fig = px.bar(**base_args)

    # Set bar color for single color bars
    if not color_col:
        fig.update_traces(
            marker_color=PRIMARY_COLOR
        )

    # Set bar border style
    fig.update_traces(
        marker_line_color=ACCENT_COLOR,
        marker_line_width=1,
    )
    
    # Implement custom styling
    fig.update_traces(hovertemplate=hovertemplate)
    fig = apply_common_styles(fig, title, x_col, y_col)

    return fig
