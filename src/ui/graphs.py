"""Graphs display module"""

import matplotlib.pyplot as plt
import streamlit as st
from core import load_data as ld
from core.statistics import mean_delay as dl
from core.statistics import season_delay_correlation
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


def display_arrival_mean_delay_history(departure_city:str, arrival_city:str) -> None:
    """Display a broken line of the mean arrival delay from the list of tuple given in arguments.

    Args:
        delay_history (list): The expected format of the history is a list of tuple under format [(month_1, mean_arrival_delay_1), ... , (month_N, mean_arrival_delay_N)]
    """
    delay_history = season_delay_correlation.compute_arrival_mean_delay_history_from_city_pair(departure_city, arrival_city)
    
    date_list, delay_list = [list(data) for data in zip(*delay_history)]
    
    fig, ax = plt.subplots()
    ax.plot(date_list, delay_list)
    ax.tick_params("x", rotation=45, rotation_mode="xtick")
    ax.set_ylabel("Retard moyen à l'arrivée")
    ax.set_xlabel("Mois de l'année")

    st.pyplot(fig)

def display_departure_city_delay_hist(ville_depart:str) -> None:
    """Display the histogram of the mean delays of a selected city from a drop down
    list, with the mean delays of both the select city, and the whole country.
    """
    # st.caption("📋 Histogrammes retards au départ par ville de départ", text_alignment="center")

    df_RetMoyDepart = ld.get_mean_departure_delay_df(ville_depart)

    fig, ax = plt.subplots()

    ax.hist(df_RetMoyDepart)
    ax.plot(dl.get_departure_city_mean_delay_df(df_RetMoyDepart, ville_depart))
    ax.plot(dl.get_national_global_delay_mean_df(df_RetMoyDepart))
    ax.legend(["Retard moyen ville", "Retard moyen France", "Retards ville"])
    ax.set_ylabel("Nombre de trains (#)")
    ax.set_xlabel("Retard moyen au départ (mn)")

    st.pyplot(fig)
