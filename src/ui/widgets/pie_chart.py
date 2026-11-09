import matplotlib.pyplot as plt
import streamlit as st


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
        autopct="%.0f%%",
        pctdistance=0.85,
        explode=explode,
    )

    # draw circle in the middle to make a pie into a donut
    # tastes way better by the way :)
    centre_circle = plt.Circle((0, 0), 0.30, fc="white")
    fig = plt.gcf()

    # Adding the circle in Pie chart
    fig.gca().add_artist(centre_circle)

    # Adding Title of chart
    plt.title("Causes possibles des retards observés (moyenne nationale)")
    st.pyplot(fig)
