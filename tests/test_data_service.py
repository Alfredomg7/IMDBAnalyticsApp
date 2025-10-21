import pytest
import polars as pl
from unittest.mock import Mock, patch
import pandas as pd
from services.data_service import DataService

@pytest.fixture
def mock_credentials():
    """Mock credentials for testing."""
    return {
        "type": "service_account",
        "project_id": "test-project",
        "private_key": "test-key"
    }


@pytest.fixture
def mock_tables_ids():
    """Mock table IDs for testing."""
    return {
        "movies_details": "movies_details_table",
        "year_genre_aggregates": "year_genre_aggregates_table",
        "runtime_distribution": "runtime_distribution_table",
        "yearly_aggregates": "yearly_aggregates_table"
    }


@pytest.fixture
def mock_bigquery_client():
    """Mock BigQuery client."""
    client = Mock()
    return client


@pytest.fixture
def data_service(mock_credentials, mock_tables_ids, mock_bigquery_client):
    """DataService instance with mocked dependencies."""
    with patch('services.data_service.get_bigquery_client', return_value=mock_bigquery_client):
        service = DataService(
            credentials=mock_credentials,
            project_id="test-project",
            dataset_id="test-dataset",
            tables_ids=mock_tables_ids,
        )
        service.client = mock_bigquery_client
        return service


class TestDataServiceInitialization:
    """Test DataService initialization."""
    
    def test_init_success(self, mock_credentials, mock_tables_ids):
        """Test successful initialization."""
        with patch('services.data_service.get_bigquery_client') as mock_get_client:
            mock_client = Mock()
            mock_get_client.return_value = mock_client
            
            service = DataService(
                credentials=mock_credentials,
                project_id="test-project",
                dataset_id="test-dataset",
                tables_ids=mock_tables_ids            )
            
            assert service.dataset_id == "test-dataset"
            assert service.base_path == "test-project.test-dataset."
            assert "movies_details" in service.tables


class TestExecuteQuery:
    """Test _execute_query method."""
    
    def test_execute_query_success(self, data_service):
        """Test successful query execution."""
        # Mock pandas DataFrame
        mock_pandas_df = pd.DataFrame({
            'title': ['Movie 1', 'Movie 2'],
            'rating': [8.5, 7.2]
        })
        
        # Mock query result
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service._execute_query("SELECT * FROM test_table")
        
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 2
        assert 'title' in result.columns
        assert 'rating' in result.columns
    
    def test_execute_query_error(self, data_service):
        """Test query execution with error."""
        data_service.client.query.side_effect = Exception("Query error")
        
        with pytest.raises(Exception, match="Query error"):
            data_service._execute_query("INVALID QUERY")

class TestGetTopMovies:
    """Test get_top_movies method."""
    
    def test_get_top_movies_success(self, data_service):
        """Test successful top movies retrieval."""
        mock_pandas_df = pd.DataFrame({
            'primary_title': ['The Godfather', 'Citizen Kane'],
            'release_year': [1972, 1941],
            'average_rating': [9.2, 8.3],
            'num_votes': [1500000, 400000],
            'genres': ['Crime,Drama', 'Drama'],
            'weighted_rating': [13800000, 3320000]
        })
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_top_movies(
            year_range=(1970, 1980),
            selected_genres=['Drama'],
            rating_threshold=(8.0, 10.0),
            limit=10
        )
        
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 2
        assert 'primary_title' in result.columns
        assert 'release_year' in result.columns
        assert 'average_rating' in result.columns
        assert 'num_votes' in result.columns
    
    def test_get_top_movies_with_genres(self, data_service):
        """Test top movies with genre filter."""
        mock_pandas_df = pd.DataFrame({
            'primary_title': ['Action Movie'],
            'genres': ['Action,Thriller'],
            'average_rating': [7.5]
        })
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_top_movies(
            year_range=(2000, 2020),
            selected_genres=['Action', 'Thriller'],
            rating_threshold=(7.0, 10.0)
        )
        
        # Verify genre filter was applied in query
        query_call = data_service.client.query.call_args[0][0]
        assert "Action" in query_call
        assert "Thriller" in query_call
        assert len(result) == 1
        assert isinstance(result, pl.DataFrame)
        assert 'primary_title' in result.columns
        
    def test_get_top_movies_no_genres(self, data_service):
        """Test top movies without genre filter."""
        mock_pandas_df = pd.DataFrame({
            'primary_title': ['Movie'],
            'average_rating': [7.5],
        })
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result

        result = data_service.get_top_movies(
            year_range=(2000, 2020),
            selected_genres=[],
            rating_threshold=(7.0, 10.0)
        )
        
        # Verify no genre filter in query
        query_call = data_service.client.query.call_args[0][0]
        assert "UNNEST(SPLIT(genres" not in query_call
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 1
    
    def test_get_top_movies_error(self, data_service):
        """Test top movies with database error."""
        data_service.client.query.side_effect = Exception("Database error")
        
        result = data_service.get_top_movies(
            year_range=(2000, 2020),
            selected_genres=[],
            rating_threshold=(7.0, 10.0)
        )
        
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 0


class TestGetYearRange:
    """Test get_year_range method."""
    
    def test_get_year_range_success(self, data_service):
        """Test successful year range retrieval."""
        mock_pandas_df = pd.DataFrame({
            'min_year': [1920],
            'max_year': [2023]
        })
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_year_range()
        
        assert result == (1920, 2023)
    
    def test_get_year_range_empty_result(self, data_service):
        """Test year range with empty result."""
        mock_pandas_df = pd.DataFrame()
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_year_range()
        
        assert result == (1900, 2025)  # Default range
    
    def test_get_year_range_error(self, data_service):
        """Test year range with error."""
        data_service.client.query.side_effect = Exception("Database error")
        
        result = data_service.get_year_range()
        
        assert result == (1900, 2025)  # Default range


class TestGetUniqueGenres:
    """Test get_unique_genres method."""
    
    def test_get_unique_genres_success(self, data_service):
        """Test successful unique genres retrieval."""
        mock_pandas_df = pd.DataFrame({
            'genre': ['Action', 'Comedy', 'Drama']
        })
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_unique_genres()
        
        assert result == ['Action', 'Comedy', 'Drama']
    
    def test_get_unique_genres_empty_result(self, data_service):
        """Test unique genres with empty result."""
        mock_pandas_df = pd.DataFrame()
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_unique_genres()
        
        assert result == []
    
    def test_get_unique_genres_error(self, data_service):
        """Test unique genres with error."""
        data_service.client.query.side_effect = Exception("Database error")
        
        result = data_service.get_unique_genres()
        
        assert result == []


class TestGetGenreTrends:
    """Test get_genre_trends method."""
    
    def test_get_genre_trends_success(self, data_service):
        """Test successful genre trends retrieval."""
        mock_pandas_df = pd.DataFrame({
            'release_year': [2020, 2021],
            'genre': ['Action', 'Comedy'],
            'movie_count': [150, 120],
            'average_rating': [7.5, 6.8],
            'total_votes': [50000, 30000]
        })
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_genre_trends(
            year_range=(2020, 2021),
            selected_genres=['Action', 'Comedy']
        )
        
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 2
        assert 'release_year' in result.columns
        assert 'genre' in result.columns
        assert 'movie_count' in result.columns
        assert 'average_rating' in result.columns
        assert 'total_votes' in result.columns
    
    def test_get_genre_trends_no_genres(self, data_service):
        """Test genre trends without genre filter."""
        mock_pandas_df = pd.DataFrame({'genre': ['Action']})
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_genre_trends(
            year_range=(2020, 2021),
            selected_genres=[]
        )
        
        # Verify no genre filter in query
        query_call = data_service.client.query.call_args[0][0]
        assert "AND genre IN" not in query_call
        assert isinstance(result, pl.DataFrame)

class TestGetRuntimeDistribution:
    """Test get_runtime_distribution method."""
    
    def test_get_runtime_distribution_success(self, data_service):
        """Test successful runtime distribution retrieval."""
        mock_pandas_df = pd.DataFrame({
            'runtime_minutes_bin': ['60-90', '90-120'],
            'movie_count': [500, 800],
            'average_rating': [7.2, 7.5],
            'min_runtime': [60, 90],
            'max_runtime': [90, 120]
        })
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_runtime_distribution(runtime_range=(60, 150))
        
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 2
        assert 'runtime_minutes_bin' in result.columns


class TestGetYearlyTrends:
    """Test get_yearly_trends method."""
    
    def test_get_yearly_trends_success(self, data_service):
        """Test successful yearly trends retrieval."""
        mock_pandas_df = pd.DataFrame({
            'release_year': [2020, 2021, 2022],
            'movie_count': [1200, 1100, 1300],
            'average_rating': [7.1, 7.2, 7.0],
            'total_votes': [500000, 480000, 520000]
        })
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_yearly_trends(year_range=(2020, 2022))
        
        assert isinstance(result, pl.DataFrame)
        assert len(result) == 3
        assert 'release_year' in result.columns


class TestEdgeCases:
    """Test edge cases and error scenarios."""
    
    def test_invalid_year_range(self, data_service):
        """Test with invalid year range."""
        mock_pandas_df = pd.DataFrame()
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        # Test with reversed year range
        result = data_service.get_top_movies(
            year_range=(2020, 1990),  # Invalid range
            selected_genres=[],
            rating_threshold=(5.0, 10.0)
        )
        
        assert isinstance(result, pl.DataFrame)
    
    def test_negative_rating_threshold(self, data_service):
        """Test with negative rating threshold."""
        mock_pandas_df = pd.DataFrame()
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_top_movies(
            year_range=(2000, 2020),
            selected_genres=[],
            rating_threshold=(-1.0, 10.0)  # Invalid rating
        )
        
        assert isinstance(result, pl.DataFrame)
    
    def test_very_large_limit(self, data_service):
        """Test with very large limit."""
        mock_pandas_df = pd.DataFrame()
        
        mock_query_result = Mock()
        mock_query_result.to_dataframe.return_value = mock_pandas_df
        data_service.client.query.return_value = mock_query_result
        
        result = data_service.get_top_movies(
            year_range=(2000, 2020),
            selected_genres=[],
            rating_threshold=(7.0, 10.0),
            limit=1000000  # Very large limit
        )
        
        assert isinstance(result, pl.DataFrame)
