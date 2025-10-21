from dash.exceptions import PreventUpdate

def validate_date_range(date_range):
    """Validate that date range is complete and valid."""
    if not date_range or len(date_range) != 2:
        raise PreventUpdate
    
    if None in date_range or '' in date_range:
        raise PreventUpdate
    
    try:
        year_start = int(date_range[0][:4])
        year_end = int(date_range[1][:4])
        
        if year_start > year_end:
            raise PreventUpdate
            
        return (year_start, year_end)
    except (TypeError, ValueError, IndexError, AttributeError):
        raise PreventUpdate