import logging
from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from config import TOP_N_MOVIES, MIN_VOTES_THRESHOLD
from components.empty_chart import create_empty_chart
from components.area_chart import create_area_chart
from components.bar_chart import create_bar_chart
from components.combo_chart import create_combo_chart
from components.dual_axis_line_chart import create_dual_axis_line_chart
from utils.serialize import df_to_base64_ipc, df_from_base64_ipc
from utils.cache import create_cache_key, deserialize_cache_data
from utils.validation import validate_date_range

def register_dashboard_callbacks(app, data_service):
    """Register callbacks for charts with frontend caching using dcc.Store"""
    
    # ========== DATA FETCHING CALLBACKS (Cache in dcc.Store with IPC) =========
    
    @app.callback(
        Output("top-movies-cache", "data"),
        [Input("year-range-filter", "value"),
         Input("genre-filter", "value"),
         Input("rating-range-filter", "value"),
         Input("runtime-range-filter", "value")],
        [State("top-movies-cache", "data")],
    )
    def fetch_top_movies(date_range, selected_genres, rating_range, runtime_range, cached_data):
        """Fetch top movies data using cache with timestamp validation."""
        year_range = validate_date_range(date_range)
        cache_key = create_cache_key(year_range, selected_genres, rating_range, runtime_range)
        cached_data = deserialize_cache_data(cached_data)
        
        # Check if cache is valid
        if cached_data and cached_data.get("cache_key") == cache_key:
            logging.info("Using cached top movies data")
            raise PreventUpdate

        logging.info("Fetching top movies data")

        top_movies_df = data_service.get_top_movies(
            year_range, selected_genres, rating_range, runtime_range=runtime_range, limit=TOP_N_MOVIES, min_votes=MIN_VOTES_THRESHOLD
        )
        
        if top_movies_df.is_empty():
            logging.warning("Top movies data is empty.")
            # Keep previous cache if available
            if cached_data and cached_data.get("data"):
                raise PreventUpdate
            return {
                "cache_key": cache_key,
                "data": None,
                "error": "No data available"
            }
        
        try:
            serialized_data = df_to_base64_ipc(top_movies_df)
            return {
                "cache_key": cache_key,
                "data": serialized_data
            }
        except Exception as e:
            logging.error(f"Error serializing top movies data: {e}")
            # Keep previous cache on serialization error
            if cached_data and cached_data.get("data"):
                raise PreventUpdate
            return {
                "cache_key": cache_key,
                "data": None,
                "error": str(e)
            }
    
    @app.callback(
        Output("genre-trends-cache", "data"),
        [Input("year-range-filter", "value"),
         Input("genre-filter", "value")],
        [State("genre-trends-cache", "data")],
    )
    def fetch_genre_trends(date_range, selected_genres, cached_data):
        """Fetch genre trends data using cache."""
        year_range = validate_date_range(date_range)
        cache_key = create_cache_key(year_range, selected_genres)
        cached_data = deserialize_cache_data(cached_data)
        
        if cached_data and cached_data.get("cache_key") == cache_key:
            logging.info("Using cached genre trends data")
            raise PreventUpdate
        
        logging.info("Fetching genre trends data")
        
        year_genre_df = data_service.get_genre_trends(year_range, selected_genres)
        
        if year_genre_df.is_empty():
            logging.warning("Genre trends data is empty.")
            if cached_data and cached_data.get("data"):
                raise PreventUpdate
            return {
                "cache_key": cache_key,
                "data": None,
                "error": "No data available"
            }
        
        try:
            serialized_data = df_to_base64_ipc(year_genre_df)
            return {
                "cache_key": cache_key,
                "data": serialized_data
            }
        except Exception as e:
            logging.error(f"Error serializing genre trends data: {e}")
            if cached_data and cached_data.get("data"):
                raise PreventUpdate
            return {
                "cache_key": cache_key,
                "data": None,
                "error": str(e)
            }
        
    @app.callback(
        Output("runtime-distribution-cache", "data"),
        [Input("runtime-range-filter", "value")],
        [State("runtime-distribution-cache", "data")],
    )
    def fetch_runtime_distribution(runtime_range, cached_data):
        """Fetch runtime distribution data using cache."""
        cache_key = create_cache_key(runtime_range)
        cached_data = deserialize_cache_data(cached_data)
        
        if cached_data and cached_data.get("cache_key") == cache_key:
            logging.info("Using cached runtime distribution data")
            raise PreventUpdate
        
        logging.info("Fetching runtime distribution data")
        
        runtime_dist_df = data_service.get_runtime_distribution(runtime_range)
        
        if runtime_dist_df.is_empty():
            logging.warning("Runtime distribution data is empty.")
            if cached_data and cached_data.get("data"):
                raise PreventUpdate
            return {
                "cache_key": cache_key,
                "data": None,
                "error": "No data available"
            }

        try:
            serialized_data = df_to_base64_ipc(runtime_dist_df)
            return {
                "cache_key": cache_key,
                "data": serialized_data
            }
        except Exception as e:
            logging.error(f"Error serializing runtime distribution data: {e}")
            if cached_data and cached_data.get("data"):
                raise PreventUpdate
            return {
                "cache_key": cache_key,
                "data": None,
                "error": str(e)
            }
        
    @app.callback(
        Output("yearly-trends-cache", "data"),
        [Input("year-range-filter", "value")],
        [State("yearly-trends-cache", "data")],
    )
    def fetch_yearly_trends(date_range, cached_data):
        """Fetch yearly trends data using cache."""
        year_range = validate_date_range(date_range)
        cache_key = create_cache_key(year_range)
        cached_data = deserialize_cache_data(cached_data)
        
        if cached_data and cached_data.get("cache_key") == cache_key:
            logging.info("Using cached yearly trends data")
            raise PreventUpdate
        
        logging.info("Fetching yearly trends data")
        
        yearly_trends_df = data_service.get_yearly_trends(year_range)
        
        if yearly_trends_df.is_empty():
            logging.warning("Yearly trends data is empty.")
            if cached_data and cached_data.get("data"):
                raise PreventUpdate
            return {
                "cache_key": cache_key,
                "data": None,
                "error": "No data available"
            }
        
        try:
            serialized_data = df_to_base64_ipc(yearly_trends_df)
            return {
                "cache_key": cache_key,
                "data": serialized_data
            }
        except Exception as e:
            logging.error(f"Error serializing yearly trends data: {e}")
            if cached_data and cached_data.get("data"):
                raise PreventUpdate
            return {
                "cache_key": cache_key,
                "data": None,
                "error": str(e)
            }
        
    # ========== CHART RENDERING CALLBACKS (Read from dcc.Store with IPC) =========
    
    @app.callback(
        [Output("top-movies-chart", "figure"),
         Output("top-movies-chart-loading", "visible")],
        [Input("top-movies-cache", "data")],
        [State("top-movies-chart", "figure")]
    )
    def render_top_movies(cached_data, current_figure):
        """Render top movies chart from cached IPC data."""
        cached_data = deserialize_cache_data(cached_data)

        if not cached_data:
            return create_empty_chart("Loading..."), True
        
        # Check for errors
        if cached_data.get("error") and not cached_data.get("data"):
            error_msg = cached_data.get("error", "Unknown error")
            logging.warning(f"Rendering empty chart due to error: {error_msg}")
            return create_empty_chart("Error rendering chart"), False
        
        # No data in cache
        if not cached_data.get("data"):
            return create_empty_chart("No data available"), False
        
        try:
            top_movies_df = df_from_base64_ipc(cached_data["data"])
            
            fig = create_bar_chart(
                df=top_movies_df,
                x_col='average_rating',
                y_col='movie_title',
                color_col='total_votes',
                horizontal=True,
                hover_name='movie_title',
                hover_data=['average_rating', 'total_votes', "genres", "release_year", "runtime_minutes", "is_adult"]
            )
            return fig, False
        except Exception as e:
            logging.error(f"Error rendering top movies chart: {e}")
            # Keep current figure if available
            if current_figure:
                return current_figure, False
            return create_empty_chart("Error rendering chart"), False
        
    @app.callback(
        [Output("genre-trends-chart", "figure"),
         Output("genre-trends-chart-loading", "visible")],
        [Input("genre-trends-cache", "data")],
        [State("genre-trends-chart", "figure")]
    )
    def render_genre_trends(cached_data, current_figure):
        """Render genre trends chart from cached IPC data."""
        cached_data = deserialize_cache_data(cached_data)
        
        if not cached_data:
            return create_empty_chart("Loading..."), True
        
        if cached_data.get("error") and not cached_data.get("data"):
            error_msg = cached_data.get("error", "Unknown error")
            logging.warning(f"Rendering empty chart due to error: {error_msg}")
            return create_empty_chart("Error rendering chart"), False
        
        if not cached_data.get("data"):
            return create_empty_chart("No data available"), False
        
        try:
            year_genre_df = df_from_base64_ipc(cached_data["data"])
            
            fig = create_area_chart(
                df=year_genre_df,
                x_col='release_year',
                y_col='total_movies',
                color_col='genre',
                hover_name='genre',
                hover_data=['total_movies', 'average_rating', 'total_votes']
            )
            return fig, False
        except Exception as e:
            logging.error(f"Error rendering genre trends chart: {e}")
            if current_figure:
                return current_figure, False
            return create_empty_chart("Error rendering chart"), False
        
    @app.callback(
        [Output("runtime-distribution-chart", "figure"),
         Output("runtime-distribution-chart-loading", "visible")],
        [Input("runtime-distribution-cache", "data")],
        [State("runtime-distribution-chart", "figure")]
    )
    def render_runtime_distribution(cached_data, current_figure):
        """Render runtime distribution chart from cached IPC data."""
        cached_data = deserialize_cache_data(cached_data)
        
        if not cached_data:
            return create_empty_chart("Loading..."), True
        
        if cached_data.get("error") and not cached_data.get("data"):
            error_msg = cached_data.get("error", "Unknown error")
            logging.warning(f"Rendering empty chart due to error: {error_msg}")
            return create_empty_chart("Error rendering chart"), False
        
        if not cached_data.get("data"):
            return create_empty_chart("No data available"), False
        
        try:
            runtime_dist_df = df_from_base64_ipc(cached_data["data"])
            
            fig = create_combo_chart(
                df=runtime_dist_df,
                x_col='runtime_bin',
                y_bar_col='total_movies',
                y_line_col='average_rating',
                hover_name='runtime_bin',
                hover_data_bar=['total_movies', 'min_runtime', 'max_runtime'],
                hover_data_line=['average_rating', 'min_runtime', 'max_runtime']
            )
            return fig, False
        except Exception as e:
            logging.error(f"Error rendering runtime distribution chart: {e}")
            if current_figure:
                return current_figure, False
            return create_empty_chart("Error rendering chart"), False

    @app.callback(
        [Output("yearly-trends-chart", "figure"),
         Output("yearly-trends-chart-loading", "visible")],
        [Input("yearly-trends-cache", "data")],
        [State("yearly-trends-chart", "figure")]
    )
    def render_yearly_trends(cached_data, current_figure):
        """Render yearly trends chart from cached IPC data."""
        cached_data = deserialize_cache_data(cached_data)
        
        if not cached_data:
            return create_empty_chart("Loading..."), True
        
        if cached_data.get("error") and not cached_data.get("data"):
            error_msg = cached_data.get("error", "Unknown error")
            logging.warning(f"Rendering empty chart due to error: {error_msg}")
            return create_empty_chart("Error rendering chart"), False
        
        if not cached_data.get("data"):
            return create_empty_chart("No data available"), False
        
        try:
            yearly_trends_df = df_from_base64_ipc(cached_data["data"])
            
            fig = create_dual_axis_line_chart(
                df=yearly_trends_df,
                x_col='release_year',
                y1_col='total_movies',
                y2_col='average_rating',
                hover_name='release_year',
                hover_data=['total_movies', 'average_rating']
            )
            return fig, False
        except Exception as e:
            logging.error(f"Error rendering yearly trends chart: {e}")
            if current_figure:
                return current_figure, False
            return create_empty_chart("Error rendering chart"), False