from datetime import datetime
from dash_iconify import DashIconify
import dash_mantine_components as dmc

def create_year_picker(id: str, type: str, min_date: datetime, max_date: datetime, title: str, placeholder: str) -> dmc.YearPickerInput:
    return dmc.YearPickerInput(
        id=id,
        type=type,
        minDate=min_date,
        maxDate=max_date,
        value=[min_date, max_date],
        label=title,
        placeholder=placeholder,
        allowSingleDateInRange=False,
        leftSection=DashIconify(icon="fa:calendar"),
        leftSectionPointerEvents="none",
    )
