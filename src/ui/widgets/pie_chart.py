import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from core import load_data as ld


def display_pie_chart(cause_list: list) -> None:

    delay_cause = [
        "Cause externe",
        "Défaillance infrastructure",
        "Gestion trafic roulant",
        "Défaillance matériel roulant",
        "Gestion trafic en gare",
        "Voyageurs en cause",
        "Cause inconnue",
    ]

    # colors
    colors = ["green", "blue", "red", "orange", "maroon", "pink", "purple"]
    # explosion
    explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)

    # Pie Chart
    plt.pie(
        cause_list,
        colors=colors,
        labels=delay_cause,
        autopct="%1.1f%%",
        pctdistance=0.85,
        explode=explode,
    )

    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc="white")
    fig = plt.gcf()

    # Adding Circle in Pie chart
    fig.gca().add_artist(centre_circle)

    # Adding Title of chart
    plt.title("Causes possibles des retards observés")
    st.pyplot(fig)
