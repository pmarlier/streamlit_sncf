"""UI widgets package, in order to spread the imports over, instead of importing them 
one by one in the modules
"""

from ui.widgets.sidebar import (
    display_sidebar,
    get_month_from_int_str,
    get_month_from_str_int,
    select_month,
    select_years,
)
from ui.widgets.train_stats_widget import (
    display_delayed_cancelled_stats_table,
    section_row,
)

" __all__ allows to import only the following modules when importing a full module"

__all__ = [
    "display_sidebar",
    "get_month_from_int_str",
    "get_month_from_str_int",
    "select_month",
    "select_years",
    "display_delayed_cancelled_stats_table",
    "section_row",
]
