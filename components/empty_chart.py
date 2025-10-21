import plotly.graph_objects as go
from config import THEME

def create_empty_chart(message="No data available"):
    """Create an empty chart with a message when no data is available."""
    fig = go.Figure()
    fig.update_layout(
        title=dict(
            text=message,
            font=dict(size=20, color=THEME["colors"]["gray"][7])
        ),
        xaxis=dict(showgrid=False, showticklabels=False, visible=False),
        yaxis=dict(showgrid=False, showticklabels=False, visible=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig