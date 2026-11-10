"""Tests for widgets from ui.widgets.

The Streamlit AppTest module is used to intercat with Streamlit website, to make sure
the correct UI and core functions outputs are generated.

#         Generated table representation with help of IA
# │
# ├── departure_city --> arrival_city
# │   Traffic state info
# │
# ├── Over the period from start_month to end_month:
# │
# ├──────────────────┬──────────────────────────────────
# │ Departure        │ delayed_trains_departure out of planned_trains trains were delayed
# │                  │
# ├──────────────────┼──────────────────────────────────
# │                  │ cancelled_trains out of planned_trains trains were cancelled
# │                  │
# ├──────────────────┴──────────────────────────────────
# │                  separator (divider)
# ├──────────────────┬──────────────────────────────────
# │ Arrival          │ delayed_trains_arrival out of planned_trains trains were delayed
# │                  │
# └──────────────────┴──────────────────────────────────

"""

import numpy as np
import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from core import load_data as ld
from core.statistics import amount_trains as am
from ui import widgets as wg


def test_display_delayed_cancelled_stats_table():
    """Tests the whole table displaying the departure and arrival statistics:
    the disposition of elements and their content.
    This is based ont the function ui.widgets.section_row,
    used to generated "Departure" and "Arrivals" sections.

    The table to be expected is (represnetation generated with AI):
    #         Tableau : at_table.columns[0]
    # │
    # ├── Metz --> Paris Est                     markdown[0]
    # │   Traffic state info
    # │
    # ├── Over the period from February to October:  markdown[1]
    # │
    # ├──────────────────┬──────────────────────────────────
    # │ Departure        │ About 1 out of 3 trains were delayed
    # │ markdown[2]      │ markdown[3]
    # ├──────────────────┼──────────────────────────────────
    # │                  │ About 1 out of 117 trains were cancelled
    # │                  │ markdown[4]
    # ├──────────────────┴──────────────────────────────────
    # │                  séparateur (divider)
    # ├──────────────────┬──────────────────────────────────
    # │ Arrival          │ About 1 out of 6 trains were delayed
    # │ markdown[5]      │ markdown[6]
    # └──────────────────┴──────────────────────────────────

    """

    total_planned_trains = 5286
    total_delayed_departure_trains = 1748
    total_delayed_arrival_trains = 908
    total_cancelled_trains = 45

    # ratio_planned_delayed_departure = round(
    #     total_planned_trains/total_delayed_departure_trains)
    # ratio_planned_delayed_arrival = round(
    #     total_planned_trains/total_delayed_arrival_trains)
    # ratio_planned_cancelled = round(
    #     total_planned_trains/total_cancelled_trains)

    departure_city = "METZ"
    arrival_city = "PARIS EST"
    start_month = 2
    end_month = 10
    selected_years = [2023, 2025]

    def run_display_delayed_cancelled_stats_table(
        departure_city, arrival_city, start_month, end_month, selected_years
    ):
        """Render a departure+arrivals section with the above given trip specs and
        trains expected stats.
        """
        import streamlit as st

        from core import load_data as ld
        from ui import widgets as wg

        ld.init()
        col, _ = st.columns(2)
        wg.display_delayed_cancelled_stats_table(
            col, departure_city, arrival_city, start_month, end_month, selected_years
        )

    at_table = AppTest.from_function(
        run_display_delayed_cancelled_stats_table,
        args=(departure_city, arrival_city, start_month, end_month, selected_years),
    ).run()

    table_markdown = at_table.columns[0].markdown
    assert at_table.markdown[0].value == (
        f"## {departure_city.title()} --> {arrival_city.title()}\n### Traffic state info"
    )
    assert at_table.markdown[1].value == (
        f"Over the period from "
        f"{wg.get_month_from_int_str(start_month)} to "
        f" {wg.get_month_from_int_str(end_month)}:"
    )
    assert table_markdown[2].value == "**Departure**"
    assert table_markdown[3].value == "About 1 out of 3 trains were delayed"
    assert table_markdown[4].value == "About 1 out of 117 trains were cancelled"
    assert table_markdown[5].value == "**Arrival**"
    assert table_markdown[6].value == "About 1 out of 6 trains were delayed"
