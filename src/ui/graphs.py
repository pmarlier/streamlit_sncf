"""Graphs display module"""

import matplotlib.pyplot as plt
import streamlit as st
from core import load_data as ld
from core.statistics import mean_delay as dl
from ui import widgets as wg

# def display_dataframe(titre: str, legende: str, df: pd.DataFrame) -> None:
#     """Affiche le dataframe importé, associé à un titre et une légende

#     Args:
#         df (pd.Dataframe): Dataframe à afficher
#         titre (str): titre à afficher
#         legende (str): légende à afficher
#     """
#     st.subheader(titre)
#     # st.subheader("📋 Retards au départ moyens par ville de départ")

#     st.dataframe(df, use_container_width=False, hide_index=True)

#     # st.caption("Retards moyens")
#     st.caption(legende)


def display_departure_city_delay_hist(ville_depart:str) -> None:
    """Display the histogram of the mean delays of a selected city from a drop down
    list, with the mean delays of both the select city, and the whole country.
    """
    st.subheader("📋 Histogrammes retards au départ par ville de départ")

    df_RetMoyDepart = ld.get_mean_departure_delay_df(ville_depart)

    fig, ax = plt.subplots()

    ax.hist(df_RetMoyDepart)
    ax.plot(dl.get_departure_city_mean_delay_df(df_RetMoyDepart, ville_depart))
    ax.plot(dl.get_national_global_delay_mean_df(df_RetMoyDepart))
    ax.legend(["Retard moyen ville", "Retard moyen France", "Retards ville"])
    ax.set_ylabel("Nombre de trains (#)")
    ax.set_xlabel("Retard moyen au départ (mn)")

    st.pyplot(fig)
