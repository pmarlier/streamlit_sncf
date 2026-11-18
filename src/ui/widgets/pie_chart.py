import matplotlib.pyplot as plt
import streamlit as st


def display_pie_chart(cause_list: list, trip_view: bool = False) -> None:

    delay_cause = [
        "Cause externe",
        "Voyageurs en cause",
        "Défaillance infrastructure",
        "Gestion trafic roulant",
        "Défaillance matériel roulant",
        "Gestion trafic en gare",
        "Cause inconnue",
    ]

    # colors mapped to cause
    # legend : SNCF responsability - red,
    # users responsability - blue,
    # bad fortune - forest green
    colors = [
        "forestgreen",
        "dodgerblue",
        "orangered",
        "orangered",
        "orangered",
        "orangered",
        "forestgreen",
    ]
    # explosion
    explode = (0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02)

    if trip_view:
        # Pie Chart
        plt.pie(
            cause_list,
            colors=colors,
            labels=delay_cause,
            autopct="%.0f%%",
            pctdistance=0.7,
            explode=explode,
            textprops={"fontsize": "xx-small"},
        )
    else:
        # Pie Chart
        plt.pie(
            cause_list,
            colors=colors,
            labels=delay_cause,
            autopct="%.0f%%",
            pctdistance=0.7,
            explode=explode,
        )

    # draw circle in the middle to make a pie into a donut
    # tastes way better by the way :)
    centre_circle = plt.Circle((0, 0), 0.30, fc="white")
    fig = plt.gcf()

    # Adding the circle in Pie chart
    fig.gca().add_artist(centre_circle)

    if trip_view:
        fig.set_size_inches(6, 2)
        fig.legend(["Hasard", "Usagers", "SNCF"], prop={"size": "xx-small"})
    else:
        fig.legend(["Hasard", "Usagers", "SNCF"])

    st.pyplot(fig)
