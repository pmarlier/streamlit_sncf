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
import pandas as pd
import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

from core import load_data as ld
from core.statistics import amount_trains as am
from ui import widgets as wg


def test_display_delayed_cancelled_stats_table(mocked_df: pd.DataFrame,):
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

    Args:
        mocked_df (pd.DataFrame): The fake Pandas DataFrame if needed
    """
    ld.init()
    # initialize load_data module with mocked dataframe
    ld.set_monthly_stats_df(mocked_df)
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
    assert at_table.markdown[0].value == "**Informations sur l'état du trafic**"
    assert at_table.markdown[1].value == (
        f"Sur la période de "
        f"{wg.get_month_from_int_str(start_month)} à "
        f" {wg.get_month_from_int_str(end_month)}:"
    )
    assert table_markdown[2].value == "**Départ**"
    assert table_markdown[3].value == "1 train sur 3 a été retardé"
    assert table_markdown[4].value == "1 train sur 117 a été annulé"
    assert table_markdown[5].value == "**Arrivée**"
    assert table_markdown[6].value == "1 train sur 6 a été retardé"


def test_section_row_edge_case_ratios():
    """Tests the section_row edge case branches, one field per branch:
    - ratio == 1: all planned trains are concerned
    - 0.95 < ratio < 1: almost all trains, avoid the "1 out of 1" approximation
    - ratio is NaN: no data available
    - ratio == 0: no concerned train was declared
    - ratio out of [0, 1]: inconsistent data
    """

    def run_section_row_edge_cases():
        """Render a single section whose fields hit every edge case branch
        of section_row."""
        import numpy as np

        from ui import widgets as wg

        wg.section_row(
            "Départ",
            [
                (1.0, "retardés"),
                (0.96, "retardés"),
                (np.nan, "retardé"),
                (0.0, "retardé"),
                (-0.5, "retardé"),
            ],
        )

    at = AppTest.from_function(run_section_row_edge_cases).run()

    markdown_values = [markdown.value for markdown in at.markdown]
    assert markdown_values == [
        "**Départ**",
        "Tous les trains prévus ont été retardés",
        "Plus de 19 trains sur 20 ont été retardés",
        "Aucune donnée n'est disponible",
        "Aucun train retardé n'a été déclaré",
        "Aucun donnée fiable n'est disponible",
    ]
