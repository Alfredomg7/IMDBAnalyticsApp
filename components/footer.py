import dash_mantine_components as dmc
from dash_iconify import DashIconify

def create_footer(data_source_url: str, github_repo_url: str) -> dmc.Group:
    """Create footer with credits and links."""
    return dmc.Group(
        [
            dmc.Text(
                [
                    "Data source: ",
                    dmc.Anchor(
                        "IMDb Non-Commercial Datasets",
                        href=data_source_url,
                        target="_blank",
                        c="yellow.7",
                        underline="hover",
                    )
                ],
                size="sm",
            ),
            dmc.Anchor(
                [
                    DashIconify(icon="mdi:github", width=20),
                    dmc.Text("View on GitHub", size="sm", ml=5)
                ],
                href=github_repo_url,
                target="_blank",
                c="yellow.6",
                underline="never",
                style={"display": "flex", "alignItems": "center"}
            )
        ],
        justify="space-between",
        align="center",
        h="100%",
        px="md"
    )
