import plotly.graph_objects as go
import polars as pl
from config import PRIMARY_COLOR, SECONDARY_COLOR
from utils.chart_styles import apply_common_styles, format_hover_template, format_label

def create_dual_axis_line_chart(
    df: pl.DataFrame,
    x_col: str,
    y1_col: str,
    y2_col: str,
    title: str = "",
    y1_color: str = None,
    y2_color: str = None,
    hover_name: str = None,
    hover_data: list = None,
    line_width: int = 3
) -> go.Figure:
    """
    Create a plotly line chart with dual Y-axes.
    
    Args:
        df: DataFrame with data
        x_col (str): Column name for x-axis
        y1_col (str): Column name for primary y-axis (left)
        y2_col (str): Column name for secondary y-axis (right)
        title (str): Chart title
        y1_color (str): Color for primary line
        y2_color (str): Color for secondary line
        hover_name (str): Column name for hover label
        hover_data (list): Additional columns to show in hover tooltip
        line_width (int): Width of the lines

    Returns:
        go.Figure: Configured dual-axis line chart
    """
    y1_label = format_label(y1_col)
    y2_label = format_label(y2_col)
    y1_color = y1_color or PRIMARY_COLOR
    y2_color = y2_color or SECONDARY_COLOR
    
    hover_name = hover_name if hover_name else x_col
    hover_data = hover_data if hover_data else [y1_col, y2_col]
    hovertemplate, custom_data_cols = format_hover_template(hover_name, hover_data)
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add primary trace (left y-axis)
    fig.add_trace(
        go.Scatter(
            x=df[x_col],
            y=df[y1_col],
            name=y1_label,
            mode='lines',
            line=dict(color=y1_color, width=line_width),
            hovertemplate=hovertemplate,
            customdata=df.select(custom_data_cols).to_numpy() if custom_data_cols else None
        )
    )
    
    # Add secondary trace (right y-axis)
    fig.add_trace(
        go.Scatter(
            x=df[x_col],
            y=df[y2_col],
            name=y2_label,
            mode='lines',
            line=dict(color=y2_color, width=line_width),
            yaxis='y2',
            hovertemplate=hovertemplate,
            customdata=df.select(custom_data_cols).to_numpy() if custom_data_cols else None
        )
    )
    

    fig = apply_common_styles(fig, title, x_col, y1_col, y2_col)
    
    
    return fig
