import numpy as np
import pytest
import streamlit as st

from streamlit.testing.v1 import AppTest

from ui.widgets import sidebar, train_stats_widget


def test_section_row():
    """Verify the train status messages output by widgets.section_row module.

    Streamlit's AppTest is used to generate a website-like UI and check displayed
    statistics in correct format: delayed departures, arrivals,
    and cancelled trains in the second column of each section.

    Cases are tested for both existing delayed/cancelled trains (return associated stat)
    or none (return "None was declared").
    """
    # ref stats
    # total_planned_trains = 1146
    # total_delayed_departure_trains = 202
    # total_delayed_arrival_trains = 230
    # total_cancelled_trains = 49

    # ratio_planned_delayed_departure = round(
    #     total_planned_trains/total_delayed_departure_trains)
    # ratio_planned_delayed_arrival = round(
    #     total_planned_trains/total_delayed_arrival_trains)
    # ratio_planned_cancelled = round(
    #     total_planned_trains/total_cancelled_trains)

    ######################
    # CASE TRAINS EXIST
    ######################

    # case departure delayed train
    def display_section_row_departure_delayed():
        """Renders a departure section with 202 delayed trains out of 1146."""
        event = "Departure"
        total_planned_trains = 1146
        total_delayed_departure_trains = 202
        from ui import widgets as wg

        wg.section_row(
            event,
            [(total_delayed_departure_trains / total_planned_trains, "retardé")],
        )

    at_departure_delayed = AppTest.from_function(
        display_section_row_departure_delayed
    ).run()
    val_col_delayed_departure = at_departure_delayed.columns[1].markdown[0].value

    # case arrival delayed train
    def display_section_row_arrival_delayed():
        """Render an arrival section with 230 delayed trains out of 1146."""
        event = "Arrival"
        total_planned_trains = 1146
        total_delayed_arrival_trains = 230
        from ui import widgets as wg

        wg.section_row(
            event,
            [(total_delayed_arrival_trains / total_planned_trains, "retardé")],
        )

    at_arrival_delayed = AppTest.from_function(
        display_section_row_arrival_delayed
    ).run()
    val_col_delayed_arrival = at_arrival_delayed.columns[1].markdown[0].value

    # case departure cancelled train
    def display_section_row_departure_cancelled():
        """Render a departure section with 49 cancelled trains out of 1146."""
        event = "Departure"
        total_planned_trains = 1146
        total_cancelled_departure_trains = 49
        from ui import widgets as wg

        wg.section_row(
            event,
            [(total_cancelled_departure_trains / total_planned_trains, "annulé")],
        )

    at_departure_cancelled = AppTest.from_function(
        display_section_row_departure_cancelled
    ).run()
    val_col_cancelled_departure = at_departure_cancelled.columns[1].markdown[0].value

    # assertions
    assert val_col_delayed_departure == "1 train sur 6 a été retardé"
    assert val_col_delayed_arrival == "1 train sur 5 a été retardé"
    assert val_col_cancelled_departure == "1 train sur 23 a été annulé"

    ######################
    # CASE NO TRAINS WERE EXPLICITELY DECLARED
    ######################

    # case departure delayed train
    def display_section_row_departure_delayed_none():
        """Render a departure delay section with zero delayed trains."""
        event = "Departure"
        total_planned_trains = 1146
        total_delayed_departure_trains = 0
        from ui import widgets as wg

        wg.section_row(
            event,
            [(total_delayed_departure_trains / total_planned_trains, "retardé")],
        )

    at_departure_delayed_none = AppTest.from_function(
        display_section_row_departure_delayed_none
    ).run()
    val_col_delayed_departure_none = (
        at_departure_delayed_none.columns[1].markdown[0].value
    )

    # case arrival delayed train
    def display_section_row_arrival_delayed_none():
        """Render an arrival delay section with zero delayed trains."""
        event = "Arrival"
        total_planned_trains = 1146
        total_delayed_arrival_trains = 0
        from ui import widgets as wg

        wg.section_row(
            event,
            [(total_delayed_arrival_trains / total_planned_trains, "retardé")],
        )

    at_arrival_delayed_none = AppTest.from_function(
        display_section_row_arrival_delayed_none
    ).run()
    val_col_delayed_arrival_none = at_arrival_delayed_none.columns[1].markdown[0].value

    # case departure cancelled train
    def display_section_row_departure_cancelled_none():
        """Render a departure section with zero cancelled trains."""
        event = "Departure"
        total_planned_trains = 1146
        total_cancelled_departure_trains = 0
        from ui import widgets as wg

        wg.section_row(
            event,
            [(total_cancelled_departure_trains / total_planned_trains, "annulé")],
        )

    at_departure_cancelled_none = AppTest.from_function(
        display_section_row_departure_cancelled_none
    ).run()
    val_col_cancelled_departure_none = (
        at_departure_cancelled_none.columns[1].markdown[0].value
    )

    # assertions
    assert val_col_delayed_departure_none == "Aucun train retardé n'a été déclaré"
    assert val_col_delayed_arrival_none == "Aucun train retardé n'a été déclaré"
    assert val_col_cancelled_departure_none == "Aucun train annulé n'a été déclaré"

    ######################
    # CASE NO DATA EXIST
    ######################

    # case departure delayed train
    def display_section_row_departure_delayed_none():
        """Render a departure delay section with no data about planned and delayed trains."""
        import numpy as np

        event = "Departure"
        ratio_delayed_departure_trains = np.nan
        from ui import widgets as wg

        wg.section_row(
            event,
            [(ratio_delayed_departure_trains, "delayed")],
        )

    at_departure_delayed_none = AppTest.from_function(
        display_section_row_departure_delayed_none
    ).run()
    val_col_delayed_departure_none = (
        at_departure_delayed_none.columns[1].markdown[0].value
    )

    # case arrival delayed train
    def display_section_row_arrival_delayed_none():
        """Render an arrival delay section with no data about planned and delayed trains."""
        import numpy as np

        event = "Arrival"
        ratio_delayed_arrival_trains = np.nan
        from ui import widgets as wg

        wg.section_row(
            event,
            [(ratio_delayed_arrival_trains, "delayed")],
        )

    at_arrival_delayed_none = AppTest.from_function(
        display_section_row_arrival_delayed_none
    ).run()
    val_col_delayed_arrival_none = at_arrival_delayed_none.columns[1].markdown[0].value

    # case departure cancelled train
    def display_section_row_departure_cancelled_none():
        """Render a departure section with no data about planned and cancelled trains."""
        import numpy as np

        event = "Departure"
        ratio_cancelled_departure_trains = np.nan
        from ui import widgets as wg

        wg.section_row(
            event,
            [(ratio_cancelled_departure_trains, "cancelled")],
        )

    at_departure_cancelled_none = AppTest.from_function(
        display_section_row_departure_cancelled_none
    ).run()
    val_col_cancelled_departure_none = (
        at_departure_cancelled_none.columns[1].markdown[0].value
    )

    # assertions
    assert val_col_delayed_departure_none == "Aucune donnée n'est disponible"
    assert val_col_delayed_arrival_none == "Aucune donnée n'est disponible"
    assert val_col_cancelled_departure_none == "Aucune donnée n'est disponible"


def test_select_month(months_list=sidebar.MONTHS_LIST):
    """Test that the dropdown list of months name under string format, when selected,
    outputs the selected month under integer format.

    ui.widgets.get_month_from_str_int module is used for the type conversion.

    Args:
        months_list (list): list of all months of the years, under string format,
        contained in MONTHS_LIST
    """

    for i, m in enumerate(months_list):
        assert sidebar.get_month_from_str_int(m) == i + 1


def test_select_years():
    """Test the multiselect box for period's years selection.
    The default years list taken from base dataframe should be initialized at
    website's entry.
    With Streamlit AppTest, years are unselected to check the widget list update.
    """

    # Initialisation du test avec le fichier de l'application
    year_start = 2018
    year_end = 2026

    def display_multiselect_years():
        """Initialize the full dataset and simulates the year selector like
        on the website.
        """
        from core import load_data as ld
        from ui import widgets as wg

        ld.init()
        wg.select_years("")

    at = AppTest.from_function(display_multiselect_years).run()

    # Vérification de l'état par défaut
    assert all(yr in at.multiselect[0].value for yr in range(year_start, year_end + 1))

    # Unselect twise a year, which should be counted as once
    at.multiselect[0].unselect(2018).unselect(2018).run()
    assert 2018 not in at.multiselect[0].value


def test_get_month_from_int_str(months_list=sidebar.MONTHS_LIST):
    """Test that input month as integer is converted into associated month's
    name in string.

    Args:
        months_list (list): list of all months of the years, under string format,
        contained in MONTHS_LIST
    """

    for i, m in enumerate(months_list):
        assert m == sidebar.get_month_from_int_str(i + 1)


def test_get_month_from_str_int(months_list=sidebar.MONTHS_LIST):
    """Test that input month as string is converted into associated month's
    digit in integer.

    Args:
        months_list (list): list of all months of the years, under string format,
        contained in MONTHS_LIST
    """

    for i, m in enumerate(months_list):
        assert i + 1 == sidebar.get_month_from_str_int(m)


def test_display_sidebar():
    """Verify trip selection through ui.widgets.display_sidebar.

    With AppTest, a given trip is selected, and the widgets outputs are tested:
    Departure and arrival cities, start and end months and years.
    """

    departure_city = "METZ"
    arrival_city = "PARIS EST"
    start_month = "Février"
    end_month = "Octobre"
    year_out = 2018

    def run_sidebar():
        """Initialize the full dataset and render the trip sidebar to simulate
        website's behavior
        """
        from core import load_data as ld
        from ui import widgets as wg

        ld.init()
        _ = wg.display_sidebar()

    at = AppTest.from_function(run_sidebar).run()

    # test choosing trip
    at_dep = at.selectbox[0].select(departure_city).run()
    at_arr = at_dep.selectbox[1].select(arrival_city).run()
    at_st = at_arr.selectbox[2].select(start_month).run()
    at_en = at_st.selectbox[3].select(end_month).run()
    at_yr = at_en.multiselect[0].unselect(year_out).run()

    dep_city = at_en.selectbox[0].value
    arr_city = at_en.selectbox[1].value
    st_mth = at_en.selectbox[2].value
    en_mth = at_en.selectbox[3].value
    yrs = at_yr.multiselect[0].value

    assert dep_city == departure_city
    assert arr_city == arrival_city
    assert st_mth == start_month
    assert en_mth == end_month
    assert year_out not in yrs
