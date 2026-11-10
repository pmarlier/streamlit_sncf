"""
Streamlit App — Informational SNCF trains delays prediction web application
============================================================================

To launch the app:
    uv sync
    cd ./ #project's root
    uv run streamlit run ./src/streamlit_sncf_app.py

The raw data file "regularite-mensuelle-tgv-aqst.csv" shall be stored in ./data/raw,
downloaded from https://ressources.data.sncf.com/explore/dataset/regularite-mensuelle-tgv-aqst/export/
"""

import os

import streamlit as st

from core import load_data as ld
from core.railway_data import railway_geo, railway_network
from core.statistics import delay_cause
from ui.carto import map_drawing, railway_drawing, st_folium
from ui.widgets import graphs, pie_chart, sidebar, train_stats_widget


def main():
    """Sets up the main page of the app by initializing data,
    UI and core modules loading."""

    # --------------------------------------------------------------------------
    # Initialisations
    # --------------------------------------------------------------------------

    if "is_app_initialized" not in st.session_state:
        # create log directory
        if not os.path.isdir("logs"):
            os.mkdir("logs")

        ld.init()
        railway_geo.init()
        railway_network.init()

        st.session_state.is_app_initialized = True
        st.session_state.first_map_load = True

    # --------------------------------------------------------------------------
    # Main page general configuration
    # --------------------------------------------------------------------------

    st.set_page_config(
        page_title="IADATA700 STreamlit SNFC app",
        page_icon="🚄",
        layout="wide",
    )

    # --------------------------------------------------------------------------
    # 1. Header
    # --------------------------------------------------------------------------

    # Create a row with 3 columns
    (logo_sncf_container, title_container, logo_telecom_paris_container) = st.columns(
        [1, 3, 1], gap="large"
    )

    with logo_sncf_container:
        if os.path.isfile("./resources/logo_sncf.png"):
            st.image("./resources/logo_sncf.png")

    with title_container:
        st.header(
            "Et si nous organisions la rencontre parfaite avec votre prochain train ?",
            text_alignment="center",
        )

    with logo_telecom_paris_container:
        if os.path.isfile("./resources/logo_tp.png"):
            st.image("./resources/logo_tp.png", width="stretch")

    # --------------------------------------------------------------------------
    # 2. Sidebar trip selection
    # --------------------------------------------------------------------------
    if "is_trip_set" not in st.session_state:
        st.session_state.is_trip_set = False

    # Note : display sidebar only if the user wants to display
    # informations on a specific railway link
    st.session_state.sidebar_state = (
        "collapsed" if not st.session_state.is_trip_set else "expanded"
    )

    st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)

    # HomePage mode - no specific railway link set
    # Display the button to pick departure and arrival

    if st.session_state.is_trip_set:
        with st.sidebar:
            sidebar.display_sidebar()
    else:
        st.markdown(
            "Mais tout d'abord, voici un aperçu des statistiques nationales",
            text_alignment="center",
        )

    # --------------------------------------------------------------------------
    # 3. Main body
    # --------------------------------------------------------------------------

    map = map_drawing.create_map()

    # sidebar active: user configuration for trip defintion in progress
    if st.session_state.is_trip_set:
        # -------------------------------------------
        # a. Delayed/cancelled stats for selected trip #
        # -------------------------------------------
        # Create a row with 2 columns
        info_container, map_container = st.columns([1, 1], gap="large")

        with info_container:
            # display monthly arrival delay graph below the map
            # only if a specific railway trip is selected
            graphs.display_monthly_arrival_delay_graph(
                departure_station=st.session_state.departure_city,
                arrival_station=st.session_state.arrival_city,
                start_month=st.session_state.start_month,
                end_month=st.session_state.end_month,
                selected_years=st.session_state.selected_years,
                actual_year=2026,
            )

            train_stats_widget.display_delayed_cancelled_stats_table(
                st.session_state.departure_city,
                st.session_state.arrival_city,
                st.session_state.start_month,
                st.session_state.end_month,
                st.session_state.selected_years,
            )

        # -------------------------------------------
        # b. France map of trip #
        # -------------------------------------------
        railway_drawing.draw_railway(
            railway_network.get_railway_data_between_cities(
                st.session_state.departure_city, st.session_state.arrival_city
            ),
            map,
        )

    # homepage mode: national data display
    else:
        # Create a row with 2 columns
        info_container, map_container = st.columns([1, 1], gap="large")

        if st.session_state.first_map_load:
            # display a loading widget
            progress_text = "Traitement des données en cours. Merci de patienter..."
            my_bar = st.progress(0, text=progress_text)

            # retrieve unique couple departure-arrival (no matter the order)
            all_railways_to_draw = []
            city_pairs = ld.get_unique_city_pairs_list()

            total_railway_number = len(city_pairs)

            for railway_index, city_pair in enumerate(city_pairs):
                if st.session_state.first_map_load:
                    ratio = railway_index / total_railway_number
                    if ratio > 0.6:
                        progress_text = (
                            "C'est presque fini. Nous vous promettons que l'attente "
                            "en vaut la peine !"
                        )

                    my_bar.progress(ratio, text=progress_text)

                departure, arrival = city_pair

                all_railways_to_draw.append(
                    railway_network.get_railway_data_between_cities(departure, arrival)
                )

            my_bar.empty()

            # never show loading bar again
            st.session_state.first_map_load = False
            st.session_state.all_railways_to_draw = all_railways_to_draw

        for railway_to_draw in st.session_state.all_railways_to_draw:
            railway_drawing.draw_railway(railway_to_draw, map)

        # TODO : Test one railway at a time

        # all_railways_to_draw = []
        # city_pairs = ld.get_unique_city_pairs_list()

        # # FAIL 17 - 20 - 35 - 50
        # # stop_index = 53

        # for railway_index, city_pair in enumerate(city_pairs):

        #     # if railway_index < stop_index:
        #     #     continue

        #     # if railway_index > stop_index:
        #     #     break

        #     departure, arrival = city_pair
        #     all_railways_to_draw.append(
        #       railway_network.get_railway_data_between_cities(departure, arrival)
        #     )

    with map_container.container(height=650):
        st_folium(map, width=740)

    with info_container:
        if st.session_state.is_trip_set:
            pie_chart.display_pie_chart(
                delay_cause.get_mean_cause_list(
                    st.session_state.departure_city, st.session_state.arrival_city
                )
            )
        else:
            pie_chart.display_pie_chart(delay_cause.get_mean_cause_list())

        if st.session_state.is_trip_set is False:
            (_, trip_button_container, _) = st.columns([1, 3, 1], gap="large")
            # Set the button to define trip configuration within the HomePage
            with trip_button_container:
                if st.button(
                    "Je veux étudier les statistiques  d'un trajet précis",
                    type="primary",
                ):
                    st.session_state.is_trip_set = True
                    st.rerun()


if __name__ == "__main__":
    main()
