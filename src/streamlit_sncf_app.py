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

import streamlit as st
from ui.carto import st_folium
from ui.carto import map_drawing, railway_drawing
from ui import graphs as gr
from ui import widgets as wg
from core.railway_data import railway_geo,railway_network
from core import load_data as ld


def main():
    """Sets up the main page of the app by initializing data, UI and core modules loading.
    """

    # --------------------------------------------------------------------------
    # Initialisations
    # --------------------------------------------------------------------------
    
    ld.init()
    railway_geo.init()
    
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

    # Create a row with 2 columns
    col1, col2, _ = st.columns([1, 3, 1], gap="large")
    with col1:
        st.image("./resources/logo_sncf.png", width = "stretch")
    with col2:
        st.title(
            "Et si nous organisions la rencontre parfaite avec votre prochain train ?", 
            text_alignment="center")
        
    # --------------------------------------------------------------------------
    # 2. Sidebar trip selection
    # --------------------------------------------------------------------------

    departure_city, arrival_city, start_month, end_month, selected_years = wg.display_sidebar()
        
    # --------------------------------------------------------------------------
    # 3. Main body
    # --------------------------------------------------------------------------

    # Create a row with 2 columns
    col1, col2 = st.columns(2)

        # -------------------------------------------
        # a. Delayed/cancelled stats for selected trip #
        # -------------------------------------------
    wg.display_delayed_cancelled_stats_table(col1, departure_city, 
                                          arrival_city, start_month, 
                                          end_month, 
                                          selected_years)
        # -------------------------------------------
        # b. France map of trip #
        # -------------------------------------------
        
    map = map_drawing.create_map()
    railway_drawing.draw_railway(railway_network.
                                 get_railway_data_from_city(departure_city), map)

    with col2:
        st_folium(map, width=725)


if __name__ == "__main__":
    main()
