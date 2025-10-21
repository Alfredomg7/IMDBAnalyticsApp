import logging
from datetime import datetime
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from config import MIN_YEAR, MAX_YEAR

def register_sidebar_callbacks(app, data_service):
    """Register callbacks for sidebar components"""

    # Callback to toggle navbar on mobile
    @app.callback(
        Output("appshell", "navbar"),
        Input("burger-menu", "opened"),
        State("appshell", "navbar"),
    )
    def toggle_navbar(opened, navbar):
        """Toggle navbar collapse state on mobile."""
        navbar["collapsed"] = {"mobile": not opened}
        return navbar
    
    # ========== DATA FETCHING CALLBACKS (Cache in dcc.Store) =========
    
    @app.callback(
        Output("year-range-cache", "data"),
        [Input("url", "pathname")],
        [State("year-range-cache", "data")]
    )
    def fetch_year_range(pathname, cached_data):
        """Fetch year range and cache in local storage."""
        # If cache exists, don't fetch again
        if cached_data and cached_data.get("min") and cached_data.get("max"):
            logging.info("Using cached year range data")
            raise PreventUpdate
        
        logging.info("Fetching year range from database")
        year_range = data_service.get_year_range()
        return {"min": year_range[0], "max": year_range[1]}

    @app.callback(
        Output("genres-cache", "data"),
        [Input("url", "pathname")],
        [State("genres-cache", "data")]
    )
    def fetch_genres(pathname, cached_data):
        """Fetch genres and cache in local storage."""
        # If cache exists, don't fetch again
        if cached_data and cached_data.get("genres"):
            logging.info("Using cached genres data")
            raise PreventUpdate
        
        logging.info("Fetching genres from database")
        genres = data_service.get_unique_genres()
        return {"genres": genres}
    
    # ========== COMPONENT RENDERING CALLBACKS (Read from dcc.Store) =========
    
    @app.callback(
        [Output("year-range-filter", "min"),
         Output("year-range-filter", "max"),
         Output("year-range-filter", "marks")],
        [Input("year-range-cache", "data")]
    )
    def render_year_range_slider(cached_data):
        """Render year range slider from cached data."""
        if cached_data and cached_data.get("min") and cached_data.get("max"):
            min_year = cached_data["min"]
            max_year = cached_data["max"]
        else:
            # Fallback to default values
            min_year = MIN_YEAR
            max_year = MAX_YEAR

        # Create datetime objects for component compatibility
        min_date = datetime(min_year, 1, 1)
        max_date = datetime(max_year, 1, 1)
        value = [min_date, max_date]

        return min_date, max_date, value
    
    @app.callback(
        Output("genre-filter", "data"),
        [Input("genres-cache", "data")]
    )
    def render_genre_filter(cached_data):
        """Render genre filter from cached data."""
        if not cached_data or not cached_data.get("genres"):
            # Default values if no cache
            return [], []
        
        genres = cached_data["genres"]
        genre_data = [{"value": genre, "label": genre} for genre in genres]
        
        return genre_data
