"""
    Démo Streamlit — Affichage trains en retard
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
        page_title="Démo - Retard moyen des trains d'une ville de départ",
        page_icon="🚄",
        layout="wide",
    )

    st.title("🚄 Démo - Retard moyen des trains d'une ville de départ")
    st.caption(
        "Première base pour dérouler le workflow complet jusqu'au déploiement continu"
    )

    departure_city = st.selectbox(
            "Ville de départ :",
            ld.get_unique_stations_df(),
        )
    # --------------------------------------------------------------------------
    # 1. Display
    # --------------------------------------------------------------------------

    # Create a row with 3 columns
    col1, col2 = st.columns(2)

    map = map_drawing.create_map()
    railway_drawing.draw_railway(railway_network.get_railway_data_from_city(departure_city), map)

    with col2:
        st_folium(map, width=725)

    with col1:
        gr.display_departure_city_delay_hist(departure_city)


if __name__ == "__main__":
    main()
