import dash_mantine_components as dmc
from dash import dcc
from config import CHART_HEIGHT, THEME, TOP_N_MOVIES, MIN_VOTES_THRESHOLD
from components.chart_card import create_chart_card

def create_dashboard():
    return dmc.Stack(
        children=[
            # Frontend cache (session storage)
            dcc.Store(id='top-movies-cache', storage_type='session'),
            dcc.Store(id='genre-trends-cache', storage_type='session'),
            dcc.Store(id='runtime-distribution-cache', storage_type='session'),
            dcc.Store(id='yearly-trends-cache', storage_type='session'),
            
            dmc.Grid([
                dmc.GridCol([
                    create_chart_card(
                        title=f"Top {TOP_N_MOVIES} Movies by Rating (At least {MIN_VOTES_THRESHOLD} Votes)",
                        chart_id="top-movies-chart",
                        height=CHART_HEIGHT,
                        border_color=THEME["colors"]["yellow"][6],
                    )
                ], span=12),
                
                dmc.GridCol([
                    create_chart_card(
                        title="Genre Popularity Over Time",
                        chart_id="genre-trends-chart",
                        height=CHART_HEIGHT,
                        border_color=THEME["colors"]["yellow"][6],
                    )
                ], span=12),
                
                dmc.GridCol([
                    create_chart_card(
                        title="Release Year Trends",
                        chart_id="yearly-trends-chart",
                        height=CHART_HEIGHT,
                        border_color=THEME["colors"]["yellow"][6],
                    )
                ], span=12),

                dmc.GridCol([
                    create_chart_card(
                        title="Movie Runtime Distribution",
                        chart_id="runtime-distribution-chart",
                        height=CHART_HEIGHT,
                        border_color=THEME["colors"]["yellow"][6],
                    )
                ], span=12),
            
            ], gutter="lg")
        ],
        gap="lg"
    )
