import plotly.graph_objects as go
# Assuming THEME is available/imported here or passed as an argument
from config import THEME, DARK_ACCENT_COLOR

def format_label(col_name: str) -> str:
    """Convert snake_case column names to Title Case for display."""
    return col_name.replace('_', ' ').title()

def apply_common_styles(fig: go.Figure, title: str = "", x_col: str = "", y_col: str = "", y2_col: str = "") -> go.Figure:
    """
    Apply common styling to plotly figures for consistency across the application.
    
    Args:
        fig (go.Figure): The plotly figure to style
        title (str): Chart title (will be hidden as titles are handled by chart cards)
        x_col (str): X-axis column name
        y_col (str): Y-axis column name
        y2_col (str): Secondary Y-axis column name (for dual-axis charts)

    Returns:
        go.Figure: The styled figure
    """
    # Style title if provided
    title_config = dict(
        text=title,
        font=dict(size=20, color=DARK_ACCENT_COLOR)
    ) if title else dict(text="")
    
    # Format axis titles to Title Case if provided
    xaxis_title = format_label(x_col) if x_col else ""
    yaxis_title = format_label(y_col) if y_col else ""

    fig.update_layout(
        # Title
        title=title_config,

        # Background and paper styling
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        
        # Font styling
        font_color=DARK_ACCENT_COLOR,
        font_family=THEME["fontFamily"],
        
        # Axis styling
        xaxis=dict(
            title=dict(
                text=xaxis_title,
                font=dict(size=18, color=DARK_ACCENT_COLOR)
            ),
            showgrid=False,
            linecolor=THEME["colors"]["gray"][5],
            tickcolor=THEME["colors"]["gray"][5],
            tickfont=dict(size=16, color=DARK_ACCENT_COLOR),
        ),
        yaxis=dict(
            title=dict(
                text=yaxis_title,
                font=dict(size=18, color=DARK_ACCENT_COLOR)
            ),
            showgrid=False,
            linecolor=THEME["colors"]["gray"][5],
            tickcolor=THEME["colors"]["gray"][5],
            tickfont=dict(size=16, color=DARK_ACCENT_COLOR),
            rangemode='tozero',
        ),
    
        
        # Legend styling
        legend=dict(
            bgcolor=THEME["colors"]["gray"][3],
            bordercolor=THEME["colors"]["gray"][3],
            borderwidth=1,
            font_color=DARK_ACCENT_COLOR,
        ),

        # Hide color axis scale if present
        coloraxis_showscale=False,

        # Margin optimization
        margin=dict(l=40, r=40, t=40, b=40),
    )
    
    # Apply secondary y-axis styling if y2_col is provided
    if y2_col:
        y2axis_title = format_label(y2_col)
        fig.update_layout(
            yaxis2=dict(
                title=dict(
                    text=y2axis_title,
                    font=dict(size=18, color=DARK_ACCENT_COLOR)
                ),
                overlaying='y',
                side='right',
                showgrid=False,
                linecolor=THEME["colors"]["gray"][5],
                tickcolor=THEME["colors"]["gray"][5],
                tickfont=dict(size=16, color=DARK_ACCENT_COLOR),
                rangemode='tozero',
            )
        )
    
    return fig

def format_hover_template(hover_name: str, hover_data: list[str]) -> tuple[str, list[str]]:
    """
    Format hover template and return custom data columns for plotly charts.
    
    Args:
        hover_name (str): Column name for hover label (main identifier)
        hover_data (list[str]): Additional columns to show in hover tooltip
        
    Returns:
        tuple: (hovertemplate_string, custom_data_columns_list)
    """
    # Initialize custom data columns list
    custom_data_cols = [hover_name] + hover_data
    
    # Construct the hovertemplate string
    template_parts = []
    custom_data_index = 0
    
    # Start with hover_name as main identifier
    template_parts.append(f'<b>%{{customdata[{custom_data_index}]}}</b>')
    custom_data_index += 1

    # Add additional hover_data columns
    for col in hover_data:
        title = format_label(col)
        template_parts.append(f'<b>{title}:</b> %{{customdata[{custom_data_index}]}}')
        custom_data_index += 1
    
    # Join all parts and include 'extra' tag to remove default info
    hovertemplate = "<br>".join(template_parts) + "<extra></extra>"
    
    return hovertemplate, custom_data_cols