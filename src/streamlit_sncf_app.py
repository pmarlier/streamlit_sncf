"""
    Streamlit App — Applications web d'informations et de prévision de retards des 
    trains SNCF
    ============================================================================

    Pour lancer l'application :
        uv sync (lance le sync des dépendances)
        cd ./
        uv run streamlit run ./streamlit/streamlit_app.py

    Le fichier `regularite-mensuelle-tgv-aqst.csv` doit contenir au minimum colonnes :
        "Gare de départ", "Retard moyen des trains en retard au départ"

    """

import streamlit as st
from ui.carto import st_folium
from ui.carto import map_drawing, railway_drawing
from ui import graphs as gr
from ui import widgets as wg
from core.railway_data import railway_geo,railway_network
from core.statistics import mean_delay as md
from core.statistics import season_delay_correlation
from core import load_data as ld

def main():
    ld.init()
    railway_geo.init()
    # --------------------------------------------------------------------------
    # Configuration générale de la page
    # --------------------------------------------------------------------------
    st.set_page_config(
        page_title="IADATA 700 App",
        page_icon="🚄",
        layout="wide",
    )

    # --------------------------------------------------------------------------
    # 1. Header
    # --------------------------------------------------------------------------
    # Columns for SNCF logo and the page title
    logo_sncf_container, title_container, logo_telecom_container = st.columns([1, 3, 1], gap="large")

    with logo_sncf_container:
        st.image("./resources/logo_sncf.png", width = "stretch")

    with title_container:
        st.title(
            "Et si nous organisions la rencontre parfaite avec votre prochain train ?", 
            text_alignment="center")
        
    with logo_telecom_container:
        st.image("./resources/logo_tp.png")
        
    # --------------------------------------------------------------------------
    # 2. Sidebar sélection voyage
    # --------------------------------------------------------------------------

    departure_city, arrival_city, start_month, end_month, selected_years = wg.display_sidebar()
        
    # --------------------------------------------------------------------------
    # 1. App display
    # --------------------------------------------------------------------------
    side_bar_container, main_body_container = st.columns([1, 5], gap="large")
    # --------------------------------------------------------------------------
    # 1. Static sidebar with 
    #       - destination / arrival menu,
    #       - top and flop rail links + destination / arrival ranking among them, 
    #       - ring of main delay cause for this line, 
    # --------------------------------------------------------------------------
        
    map = map_drawing.create_map()
    railway_drawing.draw_railway(railway_network.
                                 get_railway_data_between_cities(departure_city, arrival_city), map)
    with side_bar_container:

        departure_city = st.selectbox(
                "Ville de départ :",
                ld.get_unique_railstations_df(),
            )
        
        arrival_city = st.selectbox(
                "Ville d'arrivée :",
                ld.get_reachable_destinations_list_from_city(departure_city),
            )
    # --------------------------------------------------------------------------
    # 2. Web app body
    # --------------------------------------------------------------------------
    with main_body_container:
        # Create a row with 2 columns
        col1, col2 = st.columns([4, 2], gap="medium")

        with col1:

                # -------------------------------------------
                # a. Delayed/cancelled stats for selected trip #
                # -------------------------------------------
            wg.display_delayed_cancelled_stats_table(col1, departure_city, 
                                                arrival_city, start_month, 
                                                end_month, 
                                                selected_years)
            
            gr.display_departure_city_delay_hist(departure_city)

        # -------------------------------------------
        # b. Railway map #
        # -------------------------------------------

        map = map_drawing.create_map()
        railway_drawing.draw_railway(railway_network.get_railway_data_between_cities(departure_city, arrival_city), map)

        with col2:
            st_folium(map, width=725)


if __name__ == "__main__":
    main()