import dash_mantine_components as dmc

def create_header(burger_menu_id: str, app_title: str) -> dmc.Group:
    return dmc.Group(
    [
        dmc.Burger(id=burger_menu_id, size="sm", hiddenFrom="sm", opened=False),
        dmc.Title(app_title, order=2)
    ],
    h="100%",
    px="md",
    align="center"
)