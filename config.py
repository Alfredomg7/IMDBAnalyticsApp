import os
import logging
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Runtime Configuration
PORT = os.getenv("PORT", 8050)
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Metadata
APP_NAME = "IMDb Analytics"
APP_TITLE = f"{APP_NAME} Dashboard"
DATA_SOURCE_URL = "https://developer.imdb.com/non-commercial-datasets/"
GITHUB_REPO_URL = "https://github.com/Alfredomg7/IMDbAnalyticsApp"

# Query parameters
TOP_N_MOVIES = 20
MIN_VOTES_THRESHOLD = 1000

# Default filter values
MIN_RATING = 0
MAX_RATING = 10
MIN_YEAR = 1894
MAX_YEAR = 2025
MIN_DATE = datetime(MIN_YEAR, 1, 1)
MAX_DATE = datetime(MAX_YEAR, 1, 1)
GENRES = ["Action", "Comedy", "Drama", "Thriller", "Horror"]
RUNTIME_MIN = 0
RUNTIME_MAX = 300

# Layout Configuration
CHART_HEIGHT = 500
SIDEBAR_WIDTH = 300
HEADER_HEIGHT = 70
FOOTER_HEIGHT = 40

# Mantine Theme Configuration
THEME = {
    "colorScheme": "dark",
    "primaryColor": "yellow",
    "colors": {
        "yellow": [
            "#fff9e6",  # 0 - lightest
            "#ffecb3",  # 1
            "#ffe082",  # 2
            "#ffd54f",  # 3
            "#ffca28",  # 4
            "#ffc107",  # 5 - base yellow
            "#ffb300",  # 6 - primary shade
            "#ffa000",  # 7
            "#ff8f00",  # 8
            "#ff6f00",  # 9 - darkest
        ],
        "gray": [
            "#f8f9fa",  # 0 - lightest
            "#f1f3f4",  # 1
            "#e9ecef",  # 2
            "#dee2e6",  # 3
            "#ced4da",  # 4
            "#adb5bd",  # 5
            "#6c757d",  # 6
            "#495057",  # 7
            "#343a40",  # 8
            "#212529",  # 9 - darkest
        ]
    },
    "primaryShade": {"light": 6, "dark": 4},
    "fontFamily": "'Montserrat', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "defaultRadius": "md",
    "autoContrast": True,
    "luminanceThreshold": 0.3,
    "components": {
        "AppShellHeader": {
            "defaultProps": {
                "bg": "gray.2"
            }
        },
        "AppShellMain": {
            "defaultProps": {
                "bg": "gray.3"
            }
        },
        "AppShellNavbar": {
            "defaultProps": {
                "bg": "gray.4"
            }
        },
        "AppShellFooter": {
            "defaultProps": {
                "bg": "gray.2"
            }
        },
        "Paper": {
            "defaultProps": {
                "bg": "gray.4",
                "withBorder": True
            }
        },
        "Title": {
            "defaultProps": {
                "c": "gray.9"
            }
        },
        "Text": {
            "defaultProps": {
                "c": "gray.9"
            }
        },
        "Button": {
            "defaultProps": {
                "variant": "filled",
                "color": "yellow"
            }
        }
    },
}

# Color Palette
PRIMARY_COLOR = THEME["colors"]["yellow"][6]
SECONDARY_COLOR = THEME["colors"]["yellow"][9]
ACCENT_COLOR = THEME["colors"]["gray"][5]
DARK_ACCENT_COLOR = THEME["colors"]["gray"][7]

COLOR_CONTINUOUS_SCALE = THEME["colors"]["yellow"][2:] 
COLOR_DISCRETE_SEQUENCE = px.colors.qualitative.G10 # Use diverse colors for better contrast

# Bigquery Configuration
GOOGLE_CLOUD_CREDENTIALS = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("UNIVERSE_DOMAIN"),
}
PROJECT_ID = os.getenv("PROJECT_ID")
DATASET_ID = os.getenv("DATASET_ID")
MOVIES_DETAILS_TABLE_ID = os.getenv("MOVIES_DETAILS_TABLE_ID")
YEAR_GENRE_AGGREGATES_TABLE_ID = os.getenv("YEAR_GENRE_AGGREGATES_TABLE_ID")
YEARLY_AGGREGATES_TABLE_ID = os.getenv("YEARLY_AGGREGATES_TABLE_ID")
RUNTIME_DISTRIBUTION_TABLE_ID = os.getenv("RUNTIME_DISTRIBUTION_TABLE_ID")
TABLES_IDS = {
    "movies_details": MOVIES_DETAILS_TABLE_ID,
    "year_genre_aggregates": YEAR_GENRE_AGGREGATES_TABLE_ID,
    "yearly_aggregates": YEARLY_AGGREGATES_TABLE_ID,
    "runtime_distribution": RUNTIME_DISTRIBUTION_TABLE_ID,
}

# Configure logging with output to console and file
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

# Cache Configuration
FCD_TTL = 60 * 60 * 12 # 12 hours for frequently changing data
SCD_TTL = 60 * 60 * 24 * 7 # 1 week for slowly changing data
CACHE_CONFIG = {
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": FCD_TTL
}