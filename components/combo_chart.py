import plotly.graph_objects as go
import polars as pl
from config import PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR
from utils.chart_styles import apply_common_styles, format_hover_template, format_label

def create_combo_chart(
    df: pl.DataFrame,
    x_col: str,
    y_bar_col: str,
    y_line_col: str,
    title: str = "",
    hover_name: str = None,
    hover_data_bar: list = None,
    hover_data_line: list = None,
    bar_color: str = None,
    line_color: str = None,
    line_width: int = 3,
    secondary_y: bool = True
) -> go.Figure:
    """
    Create a plotly combo chart (bar + line) styled component.
    
    Args:
        df: DataFrame with data
        x_col (str): Column name for x-axis
        y_bar_col (str): Column name for bar y-axis
        y_line_col (str): Column name for line y-axis
        title (str): Chart title
        hover_name (str): Column name for hover label
        hover_data_bar (list): Additional columns for bar hover tooltip
        hover_data_line (list): Additional columns for line hover tooltip
        bar_color (str): Custom color for bars
        line_color (str): Custom color for line
        line_width (int): Width of the line
        secondary_y (bool): Whether to use secondary y-axis for line
        
    Returns:
        go.Figure: Configured combo chart
    """
    # Set default values
    hover_name = hover_name if hover_name else x_col
    hover_data_bar = hover_data_bar if hover_data_bar else [y_bar_col]
    hover_data_line = hover_data_line if hover_data_line else [y_line_col]
    bar_color = bar_color if bar_color else PRIMARY_COLOR
    line_color = line_color if line_color else SECONDARY_COLOR
    
    # Get formatted labels from column names
    bar_name = format_label(y_bar_col)
    line_name = format_label(y_line_col)
    
    # Format hover templates
    hovertemplate_bar, custom_data_cols_bar = format_hover_template(hover_name, hover_data_bar)
    hovertemplate_line, custom_data_cols_line = format_hover_template(hover_name, hover_data_line)
    
    # Create figure with secondary y-axis if needed
    fig = go.Figure()
    
    # Add bar trace
    fig.add_trace(
        go.Bar(
            x=df[x_col],
            y=df[y_bar_col],
            name=bar_name,
            marker_color=bar_color,
            marker_line_color=ACCENT_COLOR,
            marker_line_width=1,
            customdata=df.select(custom_data_cols_bar).to_numpy(),
            hovertemplate=hovertemplate_bar,
            yaxis='y'
        )
    )
    
    # Add line trace
    fig.add_trace(
        go.Scatter(
            x=df[x_col],
            y=df[y_line_col],
            name=line_name,
            mode='lines+markers',
            line=dict(color=line_color, width=line_width),
            marker=dict(size=8, color=line_color),
            customdata=df.select(custom_data_cols_line).to_numpy(),
            hovertemplate=hovertemplate_line,
            yaxis='y2' if secondary_y else 'y'
        )
    )
    
    # Apply common styles
    if secondary_y:
        fig = apply_common_styles(fig, title, x_col, y_bar_col, y_line_col)
    else:
        fig = apply_common_styles(fig, title, x_col, y_bar_col)
    
    return fig
