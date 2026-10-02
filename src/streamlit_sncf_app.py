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

from ui import graphs as gr
import streamlit as st

def main():
    
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

    # --------------------------------------------------------------------------
    # 1. Display
    # --------------------------------------------------------------------------

    gr.display_departure_city_delay_hist()


if __name__ == "__main__":
    main()
