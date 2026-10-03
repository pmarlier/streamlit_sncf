"""User interactions widgets definition module"""

import streamlit as st

from core import load_data as ld


# def get_departure_city_drop_down_menu() -> str:
#     """Displays a drop down menu of the departure cities of the country,
#     for the user to select one city, to be returned.

#     Returns:
#         str: Departure city
#     """

#     ville_depart = st.selectbox(
#         "Ville de départ :",
#         ld.get_unique_stations_df(),
#     )

#     return ville_depart


# def affichage_sidebar(widget: None) -> pd.Dataframe:
#     """Affiche la barre latérale avec les widgets choisis

#     Returns:
#         pd.Dataframe: le dataframe contenant les données importées
#     """

#     st.sidebar.header("⚙️ Paramètres")

#     # Liste widgets à insérer

#     df = widget

#     return df
