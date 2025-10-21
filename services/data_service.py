import logging
import polars as pl
from config import FCD_TTL, SCD_TTL
from utils.google_cloud import get_bigquery_client
from utils.cache import create_cache_key

class DataService:
    """Service to fetch data from BigQuery with optional caching."""
    
    def __init__(self, credentials: dict, project_id: str, dataset_id: str, tables_ids: dict, cache_instance=None):
        self.client = get_bigquery_client(credentials, project_id)
        self.dataset_id = dataset_id
        self.base_path = f"{project_id}.{dataset_id}."
        self.tables = {table_name: f"{self.base_path}{table_id}" for table_name, table_id in tables_ids.items()}
        self.cache = cache_instance

    def _get_cache_key(self, method_name: str, *args, **kwargs) -> str:
        """Generate cache key for method and arguments."""
        return f"{self.__class__.__name__}.{method_name}:{create_cache_key(*args, **kwargs)}"

    def _cache_get_or_set(self, method_name: str, timeout: int, func, *args, **kwargs):
        """Generic cache get or set method."""
        if not self.cache:
            return func(*args, **kwargs)
        
        cache_key = self._get_cache_key(method_name, *args, **kwargs)
        
        # Try cache first
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            logging.debug(f"Cache HIT for {method_name}")
            return cached_result
        
        # Execute and cache
        logging.debug(f"Cache MISS for {method_name}")
        result = func(*args, **kwargs)
        self.cache.set(cache_key, result, timeout=timeout)
        return result

    def _execute_query(self, query: str):
        """Execute a BigQuery SQL query and return results in the specified format."""
        try:
            return pl.from_pandas(self.client.query(query).to_dataframe())
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            raise
    
    def clear_cache(self):
        """Clear all cached data."""
        if self.cache:
            self.cache.clear()
            logging.info("Cache cleared successfully")

    def get_top_movies(self, year_range: tuple[int, int], selected_genres: list[str], rating_threshold: tuple[float, float], runtime_range: tuple[int, int] = None, limit: int = 10, min_votes: int = 100) -> pl.DataFrame:
        """Load top movies data with filters applied."""
        def _fetch(year_range, selected_genres, rating_threshold, runtime_range, limit, min_votes):
            try:
                full_table_id = self.tables['movies_details']
                genre_filter = ""
                if selected_genres:
                    genres_str = "', '".join(selected_genres)
                    genre_filter = f"AND EXISTS (SELECT 1 FROM UNNEST(SPLIT(genres, ',')) AS genre WHERE TRIM(genre) IN ('{genres_str}'))"
                
                runtime_filter = ""
                if runtime_range:
                    runtime_filter = f"AND runtime_minutes BETWEEN {runtime_range[0]} AND {runtime_range[1]}"
                
                query = f"""
                SELECT 
                    movie_title, 
                    release_year, 
                    genres, 
                    runtime_minutes, 
                    CASE 
                        WHEN is_adult = 1 THEN 'Yes' ELSE 'No'
                    END as is_adult,
                    average_rating, 
                    total_votes
                FROM `{full_table_id}`
                WHERE release_year BETWEEN {year_range[0]} AND {year_range[1]}
                AND average_rating BETWEEN {rating_threshold[0]} AND {rating_threshold[1]}
                AND total_votes >= {min_votes}
                {genre_filter}
                {runtime_filter}
                ORDER BY average_rating DESC, total_votes DESC
                LIMIT {limit}
                """
                df = self._execute_query(query)
                df = df.sort(by=["average_rating"])  # ascending for horizontal bar chart
                return df
            except Exception as e:
                logging.error(f"Error loading top movies data: {e}")
                return pl.DataFrame()
        
        return self._cache_get_or_set("get_top_movies", FCD_TTL, _fetch, year_range, selected_genres, rating_threshold, runtime_range, limit, min_votes)

    def get_year_range(self) -> tuple[int, int]:
        """Get the range of years available in movies data."""
        def _fetch():
            try:
                full_table_id = self.tables['movies_details']
                query = f"""
                SELECT MIN(release_year) AS min_year, MAX(release_year) AS max_year
                FROM `{full_table_id}`
                WHERE average_rating IS NOT NULL
                """
                df = self._execute_query(query)
                return (int(df["min_year"][0]), int(df["max_year"][0])) if len(df) > 0 else (1900, 2025)
            except Exception as e:
                logging.error(f"Error fetching year range: {e}. Using default range.")
                return (1900, 2025)
        
        return self._cache_get_or_set("get_year_range", SCD_TTL, _fetch)

    def get_unique_genres(self) -> list[str]:
        """Get list of unique genres from movies table."""
        def _fetch():
            try:
                full_table_id = self.tables['year_genre_aggregates']
                query = f"""
                SELECT DISTINCT genre
                FROM `{full_table_id}`
                ORDER BY genre
                """
                df = self._execute_query(query)
                return df["genre"].to_list() if len(df) > 0 else []
            except Exception as e:
                logging.error(f"Error fetching unique genres: {e}")
                return []
        
        return self._cache_get_or_set("get_unique_genres", SCD_TTL, _fetch)

    def get_genre_trends(self, year_range: tuple[int, int], selected_genres: list[str]) -> pl.DataFrame:
        """Get genre popularity trends over time with filters applied."""
        def _fetch(year_range, selected_genres):
            try:
                full_table_id = self.tables['year_genre_aggregates']
                genre_filter = ""
                if selected_genres:
                    genres_str = "', '".join(selected_genres)
                    genre_filter = f"AND genre IN ('{genres_str}')"
                
                query = f"""
                SELECT release_year, genre, total_movies, average_rating, total_votes
                FROM `{full_table_id}`
                WHERE release_year BETWEEN {year_range[0]} AND {year_range[1]}
                {genre_filter}
                ORDER BY release_year, genre
                """
                return self._execute_query(query)
            except Exception as e:
                logging.error(f"Error loading genre trends: {e}")
                return pl.DataFrame()
        
        return self._cache_get_or_set("get_genre_trends", FCD_TTL, _fetch, year_range, selected_genres)

    def get_runtime_distribution(self, runtime_range: tuple[int, int]) -> pl.DataFrame:
        """Get runtime distribution with filters applied."""
        def _fetch(runtime_range):
            try:
                full_table_id = self.tables['runtime_distribution']
                query = f"""
                SELECT runtime_bin, total_movies, average_rating, min_runtime, max_runtime
                FROM `{full_table_id}`
                WHERE min_runtime >= {runtime_range[0]} AND max_runtime <= {runtime_range[1]}
                ORDER BY min_runtime
                """
                return self._execute_query(query)
            except Exception as e:
                logging.error(f"Error loading runtime distribution: {e}")
                return pl.DataFrame()
        
        return self._cache_get_or_set("get_runtime_distribution", FCD_TTL, _fetch, runtime_range)

    def get_yearly_trends(self, year_range: tuple[int, int]) -> pl.DataFrame:
        """Get yearly movie release trends with filters applied."""
        def _fetch(year_range):
            try:
                full_table_id = self.tables['yearly_aggregates']
                query = f"""
                SELECT release_year, total_movies, average_rating
                FROM `{full_table_id}`
                WHERE release_year BETWEEN {year_range[0]} AND {year_range[1]}
                ORDER BY release_year
                """
                return self._execute_query(query)
            except Exception as e:
                logging.error(f"Error loading yearly trends: {e}")
                return pl.DataFrame()
        
        return self._cache_get_or_set("get_yearly_trends", FCD_TTL, _fetch, year_range)
