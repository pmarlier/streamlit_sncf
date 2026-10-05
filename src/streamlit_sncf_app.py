"""
    Streamlit App — Applications web d'informations et de prévision de retards des trains SNCF
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

    # Create a row with 2 columns
    col1, col2, _ = st.columns([1, 3, 1], gap="large")
    with col1:
        st.image("./resources/logo_sncf.png", width = "stretch")
    with col2:
        st.title("Et si nous organisions la rencontre parfaite avec votre prochain train ?", text_alignment="center")

    # --------------------------------------------------------------------------
    # 1. Display
    # --------------------------------------------------------------------------

    # Create a row with 2 columns
    col1, col2 = st.columns(2)

    with col1:
        # Create a row with 2 columns
        subcol1, subcol2 = st.columns(2)

        with subcol1:
            departure_city = st.selectbox(
                    "Ville de départ :",
                    ld.get_unique_railstations_df(),
                )
            
        with subcol2:
            arrival_city = st.selectbox(
                    "Ville d'arrivée :",
                    ld.get_reachable_destinations_list_from_city(departure_city),
                )
        gr.display_departure_city_delay_hist(departure_city)

    map = map_drawing.create_map()
    railway_drawing.draw_railway(railway_network.get_railway_data_from_city(departure_city), map)

    with col2:
        st_folium(map, width=725)



if __name__ == "__main__":
    main()
