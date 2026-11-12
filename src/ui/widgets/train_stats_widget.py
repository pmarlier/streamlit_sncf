from fractions import Fraction

import numpy as np
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from core.statistics import amount_trains as am
from ui.widgets import sidebar


def section_row(section_label: str, fields: list[tuple[float, str]]) -> None:
    """Displays information contained in fields input, named after section_label input,
    under the format of a 2 columns table : | section_label | field1
                                            |               | field2
                                            |               | ....
                                            |               | fieldN

    Ratios between 0 (excluded) and 1 (excluded) of trains delayed/cancelled
    are displayed as approximate proportions ("X out of Y trains").
    Very low and very high ratios are handled separately to avoid
    misleading approximations.
    Missing values, zero ratios and invalid ratios are handled separately.

    Args:
        section_label (str): Label of the section, contained in the first column.

        fields (list): list of fields, tuples containing a ratio and a status.
        The ratio represents the number of delayed/cancelled trains
        divided by the number of planned trains over the selected period.
        First field is displayed in the second column,
        same line as the section_label. Other fields are stacked on the following rows
        on the second column.
    """

    cols = st.columns([1, 2])
    cols[0].markdown(f"**{section_label}**")

    for index, (ratio, status) in enumerate(fields):
        # for index, (label, count, total, status) in enumerate(fields):
        if ratio > 0 and ratio <= 1:
            if ratio == 1:
                train_info_str = f"Tous les trains prévus ont été {status}"
            elif ratio > 0.95:
                # avoid incorrectly approximating a ratio to "1 out of 1"
                train_info_str = f"Plus de 19 trains sur 20 ont été {status}"
            elif ratio < 0.05:
                # avoid incorrectly approximating a ratio to "0 out of 1"
                train_info_str = (
                    f"1 train sur {round(1 / ratio)} a été {status}"
                )
            else:
                # generate a set of the most easy-to-understand approximate fractions
                # with a denominator of 2 to 6, 10 or 20
                # or with a numerator of 1 and a denominator of at most 20
                fractions = {
                    Fraction(n, d)
                    for d in range(2, 21)
                    for n in range(1, d)
                    if d <= 6 or d in (10, 20) or n == 1
                }

                # Select the closest easy-to-understand fraction to the actual ratio
                fraction = min(
                    fractions, key=lambda f: (abs(float(f) - ratio), f.denominator)
                )

                train_info_str = (
                    f"{fraction.numerator} train sur "
                    f"{fraction.denominator} a été {status}"
                )
        elif np.isnan(ratio):
            train_info_str = "Aucune donnée n'est disponible"
        elif ratio == 0:
            train_info_str = f"Aucun train {status} n'a été déclaré"
        else:
            train_info_str = "Aucun donnée fiable n'est disponible"

        if index == 0:
            # cols[1].markdown(label)
            with cols[1]:
                st.write(train_info_str)
        else:
            _, sub_input_col = st.columns([1, 2])
            # _, sub_label_col, sub_input_col = st.columns([1, 2, 3])
            # sub_label_col.markdown(label)
            with sub_input_col:
                st.write(train_info_str)


def display_delayed_cancelled_stats_table(
    col: DeltaGenerator,
    departure_city: str,
    arrival_city: str,
    start_month: str,
    end_month: str,
    selected_years: np.ndarray,
) -> None:
    """Displays delayed and cancelled train ratios in the given column.
    The ratios are displayed as approximate fractions ("X out of Y trains").
    The statistics are the ratios computed over a given months/years period,
    for a given departure and arrival cities.

    Args:
        col (DeltaGenerator): body column (container) to place the table in
        departure_city (str): departure city to compute the statistics
        arrival_city (str): arrival city
        start_month (str): first month of the time period for a given year
        end_month (str): last month of the time period
        selected_years (np.ndarray): np.ndarray of selected years to
            compute the statistics
    """
    # departure_icon_container, railway_icon_container, arrival_icon_container = (
    #     st.columns([1.5, 2, 1.5], gap="large")
    # )

    # with departure_icon_container.container(height=10):
    #     st.image("./resources/departure_arrival_icon.png")

    # with railway_icon_container.container(height=10):
    #     st.image("./resources/railway_tracks_icon.png")

    # with arrival_icon_container.container(height=10):
    #     st.image("./resources/departure_arrival_icon.png")

    # departure_city_container, _, arrival_city_container = st.columns([2, 1, 2])

    # with arrival_city_container:
    #     st.markdown(f"{departure_city}")

    # with departure_city_container:
    #     st.markdown(f"{arrival_city}")

    with col:
        st.markdown(
            "**Informations sur l'état du trafic**"
        )

        st.markdown(
            f"Sur la période de "
            f"{sidebar.get_month_from_int_str(start_month)} à "
            f" {sidebar.get_month_from_int_str(end_month)}:"
        )

        # Departure: Delay + Cancelled
        with st.container(border=True):
            section_row(
                "Départ",
                [
                    (
                        am.get_ratio_delayed_departure_trains(
                            departure_city,
                            arrival_city,
                            start_month,
                            end_month,
                            selected_years,
                        ),
                        "retardé",
                    ),
                    (
                        am.get_ratio_cancelled_trains(
                            departure_city,
                            arrival_city,
                            start_month,
                            end_month,
                            selected_years,
                        ),
                        "annulé",
                    ),
                ],
            )

            st.divider()

            # Arrival: Delay only
            section_row(
                "Arrivée",
                [
                    (
                        am.get_ratio_delayed_arrival_trains(
                            departure_city,
                            arrival_city,
                            start_month,
                            end_month,
                            selected_years,
                        ),
                        "retardé",
                    ),
                ],
            )


def display_departure_arrival_stations_title(
    col: DeltaGenerator,
    departure_city: str,
    arrival_city: str,
) -> None:
    """Displays as a title the departure and arrival cities,
    based on the ones selected in the sidebar dropdown lists.

    Args:
        col (DeltaGenerator): body column (container) to place the table in
        departure_city (str): departure city to compute the statistics
        arrival_city (str): arrival city
    """

    with col:
        st.markdown(f"## {departure_city.title()} → {arrival_city.title()}")