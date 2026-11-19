"""
Streamlit App — Informational SNCF trains delays prediction web application
============================================================================

To launch the app:
    uv sync
    cd .
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
        sidebar.init()
        train_stats_widget.init()
        delay_cause.init()
        map_drawing.init()

        st.session_state.is_app_initialized = True
        st.session_state.first_map_load = True
        # homepage mode
        st.session_state.is_trip_set = False
        st.session_state.show_homepage = False

    # --------------------------------------------------------------------------
    # Main page general configuration
    # --------------------------------------------------------------------------

    st.set_page_config(
        page_title="IADATA700 Streamlit SNFC app",
        page_icon="🚄",
        layout="wide",
    )

    # --------------------------------------------------------------------------
    # 1. Header
    # --------------------------------------------------------------------------

    # Create a row with 3 columns
    (logo_sncf_container, title_container, logo_telecom_paris_container) = st.columns(
        [1, 10, 1]
    )

    st.markdown(
        """
    <style>
    .title-font {
        font-size:25px !important;
        font-weight:bold;
    }
    .subtitle-font {
        font-size:18px !important;
        font-weight:bold;
    }
    .st-key-trip_set .stButton button {
        background-color: #F5F5F5;
        width: 300px; 
    }
    .st-key-homepage .stButton button {
        background-color: #F5F5F5;
        width: 300px; 
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    with logo_sncf_container:
        if os.path.isfile("./resources/logo_sncf.png"):
            st.image("./resources/logo_sncf.png")

    with logo_telecom_paris_container:
        if os.path.isfile("./resources/logo_tp.png"):
            st.image("./resources/logo_tp.png")

    with title_container:
        st.markdown(
            '<p class="title-font">Et si nous organisions la rencontre '
            "parfaite avec votre prochain train ?</p>",
            unsafe_allow_html=True,
            text_alignment="center",
        )

        # if st.session_state.is_trip_set is False:
        # trick to center buttons within the page
        (_, homepage_button_container, trip_button_container, _) = st.columns(
            [1, 2, 2, 1]
        )
        # Set the button to define trip configuration within the HomePage
        with trip_button_container:
            if st.button(
                "Etudier les statistiques d'un trajet précis",
                key="trip_set",
            ):
                st.session_state.is_trip_set = True
                st.session_state.show_homepage = False

        # Set the button to display homepage
        with homepage_button_container:
            if st.button(
                "Visualiser les statistiques nationales",
                key="homepage",
            ):
                st.session_state.is_trip_set = False
                st.session_state.show_homepage = True

    # --------------------------------------------------------------------------
    # 2. Sidebar trip selection
    # --------------------------------------------------------------------------

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

    # --------------------------------------------------------------------------
    # 3. Main body
    # --------------------------------------------------------------------------
    map = map_drawing.create_map()

    # Create a row with 2 columns
    if st.session_state.is_trip_set:
        # column proportion depends on the display mode
        info_container, map_container = st.columns([2.5, 1.5])
    else:
        info_container, map_container = st.columns([1, 1])

    # sidebar active: user configuration for trip defintion in progress
    if st.session_state.is_trip_set:
        with info_container:
            # -------------------------------------------
            # a. Monthly arrival delay graph for selected trip #
            # -------------------------------------------

            with st.container(border=True, height=400):
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
            with st.container(border=True, height=400):
                # display pie chart of delay cause
                pie_chart.display_pie_chart(
                    delay_cause.get_mean_cause_list(
                        st.session_state.departure_city,
                        st.session_state.arrival_city,
                    ),
                    st.session_state.is_trip_set,  # flag to identify display mode
                )

        with map_container:
            with st.container(height=450):
                # update lat/long/zoom parameter to match with the new widget size
                map = map_drawing.create_map(latitude=41.7, longitude=2.34, zoom=5)
                # with st.container(border=True):
                # -------------------------------------------
                # b. France map of trip #
                # -------------------------------------------
                railway_drawing.draw_railway(
                    railway_network.get_railway_data_between_cities(
                        st.session_state.departure_city, st.session_state.arrival_city
                    ),
                    map,
                    None,
                )
                st.markdown(
                    f"Retard moyen à l'arrivée pour {st.session_state.departure_city} "
                    f"- {st.session_state.arrival_city}",
                    text_alignment="center",
                )
                st_folium(map, width=500, render=True)

            with st.container(height=350):
                frame = st.container()
                # display delayed / cancelled train widget
                # -------------------------------------------
                # c. Delayed/cancelled stats for selected trip #
                # -------------------------------------------
                train_stats_widget.display_delayed_cancelled_stats_table(
                    frame,
                    st.session_state.departure_city,
                    st.session_state.arrival_city,
                    st.session_state.start_month,
                    st.session_state.end_month,
                    st.session_state.selected_years,
                )

    # homepage mode: national data display
    else:
        if st.session_state.show_homepage:
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
                                "C'est presque fini. Nous vous promettons que "
                                "l'attente en vaut la peine !"
                            )

                        my_bar.progress(ratio, text=progress_text)

                    departure, arrival = city_pair

                    all_railways_to_draw.append(
                        railway_network.get_railway_data_between_cities(
                            departure, arrival
                        )
                    )

                my_bar.empty()

                # never show loading bar again
                st.session_state.first_map_load = False
                st.session_state.all_railways_to_draw = all_railways_to_draw
            # -------------------------------------------
            # d. Pie chart #
            # -------------------------------------------
            with info_container.container(height=750):
                # Adding Title of chart
                st.markdown(
                    '<p class="subtitle-font">Causes et responsabilités des '
                    "retards à l'arrivée (moyenne nationale de 2018 à 2026)</p>",
                    unsafe_allow_html=True,
                    text_alignment="center",
                )
                pie_chart.display_pie_chart(
                    delay_cause.get_mean_cause_list(),
                    st.session_state.is_trip_set,  # flag to identify display mode
                )
            # -------------------------------------------
            # d. Map #
            # -------------------------------------------
            with map_container.container(height=750):
                st.markdown(
                    '<p class="subtitle-font">Cartographie des retards moyens à '
                    "l'arrivée par lignes (statistiques de 2018 à 2026)</p>",
                    unsafe_allow_html=True,
                    text_alignment="center",
                )

                delay_range = st.slider(
                    "Plage de retard (en minutes) pour les lignes affichées",
                    min_value=map_drawing.MIN_DELAY_VALUE,
                    max_value=map_drawing.MAX_DELAY_VALUE,
                    value=(map_drawing.MIN_DELAY_VALUE, map_drawing.MAX_DELAY_VALUE),
                )

                for railway_to_draw in st.session_state.all_railways_to_draw:
                    railway_drawing.draw_railway(railway_to_draw, map, delay_range)

                st_folium(map, width=850, render=True)


if __name__ == "__main__":
    main()
