import matplotlib.pyplot as plt
import streamlit as st


def display_pie_chart(cause_list: list, trip_view: bool = False) -> None:
    """Display the pie chart showing all the delay causes given as input
    argument, adapting the display to the screen configuration

    Args:
        cause_list (list): A list storing all the possible delay causes,
        following the hereafter order:
            cause_list[0] : "Cause externe",
            cause_list[1] : "Voyageurs en cause",
            cause_list[2] : "Défaillance infrastructure",
            cause_list[3] : "Gestion trafic roulant",
            cause_list[4] : "Défaillance matériel roulant",
            cause_list[5] : "Gestion trafic en gare",
            cause_list[6] : "Cause inconnue",

        trip_view (bool, optional): the flag to indicate the screen configuration.
         If set to True, the screen is in homepage configuration. Defaults to False.
    """
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
    # add margin from bottom:
    plt.subplots_adjust(bottom=0.25, wspace=0.2, hspace=0.4)

    if trip_view:
        fig.set_size_inches(5.5, 2.3)
        fig.legend(
            ["Hasard", "Usagers", "SNCF"], prop={"size": "xx-small"}, loc="center right"
        )
    else:
        fig.set_size_inches(5.5, 5)
        fig.legend(["Hasard", "Usagers", "SNCF"], loc="upper right")

    st.pyplot(fig)
