from dash import Dash, dcc
from flask_caching import Cache
import dash_mantine_components as dmc
from sidebar.layout import create_sidebar
from sidebar.callbacks import register_sidebar_callbacks
from dashboard.layout import create_dashboard
from dashboard.callbacks import register_dashboard_callbacks
from components.header import create_header
from components.footer import create_footer
from services.data_service import DataService
from config import (
    APP_NAME, APP_TITLE, CACHE_CONFIG, THEME,
    SIDEBAR_WIDTH, HEADER_HEIGHT, FOOTER_HEIGHT,
    GOOGLE_CLOUD_CREDENTIALS, PROJECT_ID,
    DATASET_ID, TABLES_IDS, DATA_SOURCE_URL, GITHUB_REPO_URL
)

# Initialize Dash app
app = Dash(__name__, title=APP_NAME)
server = app.server

# Initialize in-memory cache
cache = Cache(app.server, config=CACHE_CONFIG)

# Initialize data querying service
data_service = DataService(
    credentials=GOOGLE_CLOUD_CREDENTIALS,
    project_id=PROJECT_ID,
    dataset_id=DATASET_ID,
    tables_ids=TABLES_IDS,
    cache_instance=cache
)

# Configure Mantine theme and AppShell layout
app.layout = dmc.MantineProvider(
    theme=THEME,
    children=[
        dcc.Location(id="url", refresh=False),
        dmc.AppShell(
            [
                dmc.AppShellHeader(
                    create_header(
                        burger_menu_id="burger-menu",
                        app_title=APP_TITLE
                    )
                ),
                dmc.AppShellNavbar(
                    id="navbar",
                    children=create_sidebar(),
                    p=0
                ),
                dmc.AppShellMain(create_dashboard()),
                dmc.AppShellFooter(create_footer(
                    data_source_url=DATA_SOURCE_URL,
                    github_repo_url=GITHUB_REPO_URL
                ))
            ],
            header={"height": HEADER_HEIGHT},
            footer={"height": FOOTER_HEIGHT},
            navbar={
                "width": SIDEBAR_WIDTH,
                "breakpoint": "sm",
                "collapsed": {"mobile": True}
            },
            padding="md",
            id="appshell"
        )
    ]
)


# Register callback functions
register_sidebar_callbacks(app, data_service)
register_dashboard_callbacks(app, data_service)

if __name__ == "__main__":
    from config import DEBUG, PORT

    app.run(port=PORT, debug=DEBUG)