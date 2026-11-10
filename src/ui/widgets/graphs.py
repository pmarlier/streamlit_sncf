"""Graphs display module"""

import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from core import load_data as ld
from core.statistics import delay_seasonal_distribution as dsd
from core.statistics import mean_delay as dl

# from ui import widgets as wg

# TO DO : verify with Pierre if all these imports are still usefull

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


def display_departure_city_delay_hist(ville_depart: str) -> None:
    """Display the histogram of the mean delays of a selected city from a drop down
    list, with the mean delays of both the select city, and the whole country.
    """
    # st.caption("📋 Histogrammes retards au départ
    # par ville de départ", text_alignment="center")

    df_RetMoyDepart = ld.get_mean_departure_delay_df(ville_depart)

    fig, ax = plt.subplots()

    ax.hist(df_RetMoyDepart)
    ax.plot(dl.get_departure_city_mean_delay_df(df_RetMoyDepart, ville_depart))
    ax.plot(dl.get_national_global_delay_mean_df(df_RetMoyDepart))
    ax.legend(["Retard moyen ville", "Retard moyen France", "Retards ville"])
    ax.set_ylabel("Nombre de trains (#)")
    ax.set_xlabel("Retard moyen au départ (mn)")

    st.pyplot(fig)


def display_monthly_arrival_delay_graph(
    departure_station: str,
    arrival_station: str,
    start_month: int,
    end_month: int,
    selected_years: list[int],
    actual_year: int = 2026,
) -> None:
    """Display a graph of monthly mean arrival delays
    for a selected railway line.

    Compare the monthly mean delays of the actual year with
    the median of the monthly mean delays from selected previous years.

    The graph also displays historical minimum, maximum and quartiles,
    when enough observations are available.
    The months selected by the user are highlighted.

    Args:
        departure_station (str): departure railway station
        arrival_station (str): arrival railway station
        start_month (int): first month of the selected period (included)
        end_month (int): last month of the selected period (included)
        selected_years (list[int]): years selected by the user.
            The actual year wil be excluded from historical calculations if needed.
        actual_year (int, optional): year whose observations are compared
            with the historical distribution. Defaults to 2026.
    """

    # get the statistics from the backend
    df = dsd.get_monthly_mean_arrival_delay_global_dataframe(
        departure_station=departure_station,
        arrival_station=arrival_station,
        start_month=1,
        end_month=12,
        years_list=selected_years,
        data_df=ld.df,
        actual_year=actual_year,
    )

    # display a message if no data available
    if df.empty or (
        df["median"].isna().all() and df["mean_arrival_delay_actual_year"].isna().all()
    ):
        st.info("No data available for the selected period.")
        return

    # create the empty graph
    graph = go.Figure()

    # display the historical distribution color zones
    for _, row in df.iterrows():
        month = row["month"]  # get the number of the month

        # verify if the month is selected
        # True if selected months:
        is_selected = start_month <= month <= end_month

        # caracteristics of the color zones
        # between the minimum and maximum
        # if the 2 values exist:
        if pd.notna(row["minimum"]) and pd.notna(row["maximum"]):
            graph.add_shape(
                type="rect",  # define a rectangle
                x0=month - 0.5,  # beginning of it on X axis
                x1=month + 0.5,  # end on X axis
                y0=row["minimum"],  # beginning of it on Y axis
                y1=row["maximum"],  # end on Y axis
                # 2 colors to differentiate the selected period:
                fillcolor=(
                    "rgba(245, 158, 11, 0.18)"
                    if is_selected  # Orange
                    else "rgba(100, 116, 139, 0.15)"  # Grey
                ),
                line_width=0,  # no edge around the rectangle
                layer="below",  # color zones are behind the curves
            )

        # caracteristics of the color zones
        # between the Q1 and Q3
        # if the 2 values exist:
        if pd.notna(row["q1"]) and pd.notna(row["q3"]):
            graph.add_shape(
                type="rect",  # define a rectangle
                x0=month - 0.5,  # beginning on X axis
                x1=month + 0.5,  # end on X axis
                y0=row["q1"],  # beginning of it on Y axis
                y1=row["q3"],  # end on Y axis
                # 2 colors to differentiate the selected period:
                fillcolor=(
                    "rgba(245, 158, 11, 0.35)"
                    if is_selected  # darf orange
                    else "rgba(100, 116, 139, 0.30)"  # dark grey
                ),
                line_width=0,  # no edge around the rectangle
                layer="below",  # color zones are behind the curves
            )

    # prepare information for hover tooltips
    historical_info = []

    for _, row in df.iterrows():  # loop through the months
        # number of historical years (observations):
        historical_years = int(row["number_historical_year_observations"])

        if pd.notna(row["sum_arr_delayed_trains"]):
            # convert to int to be sure:
            delayed_trains = int(row["sum_arr_delayed_trains"])
        else:
            delayed_trains = "Unknown"

        # add the values to the list:
        historical_info.append([historical_years, delayed_trains])

    # historical median
    graph.add_trace(
        go.Scatter(  # create a line
            x=df["month"],
            y=df["median"],
            mode="lines+markers",  # display line and points
            name="Median of previous years' mean delays",  # name in the legend
            line=dict(color="gray", dash="dash"),  # dashed line
            showlegend=False,  # hide this in the legend
            # No connexion between points separated by missing values:
            connectgaps=False,
            # additionnal data displayed on hover
            # stored in customdata:
            customdata=historical_info,
            hovertemplate=(  # text on hover of a point:
                "Median of selected previous years: %{y:.1f} min"
                # number of years:
                "<br>Selected previous years with valid observations: %{customdata[0]}"
                "<br>Delayed trains: %{customdata[1]}"  # delayed trains
                "<extra></extra>"  # hide the second section of the box
            ),
        )
    )

    # prepare actual year train counts for hover tooltips
    actual_year_info = []

    for count in df["number_arr_delayed_trains_actual_year"]:
        if pd.notna(count):
            delayed_trains = int(count)
        else:
            delayed_trains = "Unknown"

        actual_year_info.append([delayed_trains])

    # actual year mean arrival delays
    graph.add_trace(
        go.Scatter(
            x=df["month"],
            y=df["mean_arrival_delay_actual_year"],
            mode="lines+markers",
            name=str(actual_year),
            line=dict(color="#93C5FD", width=2),
            connectgaps=False,
            legendgroup="actual_year",  # group in one legend
            # hide it in the legend to show the dark blue:
            showlegend=False,
            customdata=actual_year_info,
            hovertemplate=(
                f"Mean arrival delay {actual_year}: %{{y:.1f}} min"
                "<br>Delayed trains: %{customdata[0]}"
                "<extra></extra>"
            ),
        )
    )

    # identify the months selected by the user
    selected_months = df["month"].between(start_month, end_month)

    # highlight the historical median for selected months
    graph.add_trace(
        go.Scatter(
            x=df["month"],
            y=df["median"].where(selected_months),
            mode="lines+markers",
            name="Median of previous years' mean delays",
            line=dict(color="#EA580C", dash="dash", width=3),
            connectgaps=False,
            showlegend=True,
            hoverinfo="skip",
        )
    )

    # highlight the actual year for selected months
    graph.add_trace(
        go.Scatter(
            x=df["month"],
            y=df["mean_arrival_delay_actual_year"].where(selected_months),
            mode="lines+markers",
            name=str(actual_year),
            line=dict(color="#2563EB", width=3),
            connectgaps=False,
            legendgroup="actual_year",  # group in one legend
            showlegend=True,
            hoverinfo="skip",
        )
    )
    graph.update_layout(
        legend=dict(
            x=0.5,
            y=1.1,
            traceorder="normal",
            font=dict(size=12),
        )
    )
    # configure the graph
    graph.update_layout(
        title=dict(
            text="Monthly mean arrival delays",
            subtitle=dict(
                text=f"Compare {actual_year} and statistics "
                "of the selected previous years",
                font=dict(size=12),
            ),
        ),
        xaxis=dict(
            title="Month",  # title of X axis
            # define manually the graduations and the labels:
            tickmode="array",
            tickvals=list(range(1, 13)),
            ticktext=[
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
            # let space to display the rectangles
            # of first and last months:
            range=[0.5, 12.5],
        ),
        yaxis_title="Mean arrival delay (minutes)",
        hovermode="x unified",
        height=450,
    )

    # display in Streamlit
    st.plotly_chart(graph, width="stretch")

    # st.caption(
    #     # note : it requires 2 spaces before \n
    #     "Light band for each month: minimum–maximum of selected previous years.  \n"
    #     "Dark band for each month: interval between Q1 and Q3 "
    #     "of selected previous years.  \n"
    #     "Bands are displayed only when enough observations are available."
    # )
