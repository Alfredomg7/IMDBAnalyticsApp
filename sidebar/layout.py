from dash import dcc
import dash_mantine_components as dmc
from config import (
    MIN_DATE, MAX_DATE, GENRES, MIN_RATING, MAX_RATING,
    RUNTIME_MIN, RUNTIME_MAX, PRIMARY_COLOR
)
from components.range_slider import create_range_slider
from components.multi_select import create_multi_select
from components.year_picker import create_year_picker

def create_sidebar():
    """Create sidebar with default values, data will be populated via callbacks."""
    
    return dmc.Stack(
        children=[
            # Local storage for caching
            dcc.Store(id="year-range-cache", storage_type="local"),
            dcc.Store(id="genres-cache", storage_type="local"),
            
            dmc.Title("Filters", order=3, mb=20, c="gray.8"),

            # Year Range Filter
            create_year_picker(
                id="year-range-filter",
                type="range",
                min_date=MIN_DATE,
                max_date=MAX_DATE,
                title="Release Year Range",
                placeholder="Select year range"
            ),
            
            # Genre Filter
            create_multi_select(
                id="genre-filter",
                values=GENRES,
                title="Genres",
                color=PRIMARY_COLOR
            ),
            
            # Runtime Range Filter
            create_range_slider(
                id="runtime-range-filter",
                min_value=RUNTIME_MIN,
                max_value=RUNTIME_MAX,
                title="Runtime Range (min)",
                step=1,
                mark_step=60
            ),

            # Rating Range Filter
            create_range_slider(
                id="rating-range-filter",
                min_value=MIN_RATING,
                max_value=MAX_RATING,
                title="Rating Range",
                step=0.1,
                mark_step=1
            ),
        ],
        p=20,
        gap="md"
    )