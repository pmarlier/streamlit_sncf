"""Data loading module"""

import pandas as pd
import numpy as np
import streamlit as st
import itertools
import datetime as dt
from core.data_preprocessing import preprocess_data

CSV_PATH = "./data/raw/regularite-mensuelle-tgv-aqst.csv"

# to simplify access to the column, keys are made up to avoid typing endless column names
DATE_KEY = "Date"
MONTH_KEY = "month"
YEAR_KEY = "year"
DEPARTURE_STATION_KEY = "Gare de départ"
ARRIVAL_STATION_KEY = "Gare d'arrivée"
MEAN_DEPARTURE_DELAY_KEY = "Retard moyen des trains en retard au départ"
MEAN_ARRIVAL_DELAY_KEY = "Retard moyen des trains en retard à l'arrivée"
MENSUAL_CANCELLED_TRAINS_KEY = "Nombre de trains annulés"
MENSUAL_PLANNED_TRAINS_KEY = "Nombre de circulations prévues"
MENSUAL_DELAYED_DEPARTURE_TRAINS_KEY = "Nombre de trains en retard au départ"
MENSUAL_DELAYED_ARRIVAL_TRAINS_KEY = "Nombre de trains en retard à l'arrivée"


@st.cache_data  # mémorise le résultat d’une fonction pour éviter de la recalculer à
# chaque interaction Streamlit.

def load_csv_df(source: str = CSV_PATH) -> pd.DataFrame:
    """Charge un fichier csv, de séparateurs ";", utilisé pour l'analyse de données.
    Filtre les colonnes utiles, et convertit en deux colonnes "year" et "month" la 
    colonne "Date"

    Args:
        source (str): input de type input = st.sidebar.file_uploader()

    Returns:
        df (pd.DataFrame): retourne le csv converti en DataFrame
    """
    df = pd.read_csv(source, sep=";")
    df = preprocess_data(df)
    
    df = df[[DATE_KEY, DEPARTURE_STATION_KEY, ARRIVAL_STATION_KEY, 
             MEAN_DEPARTURE_DELAY_KEY, MEAN_ARRIVAL_DELAY_KEY, 
             MENSUAL_CANCELLED_TRAINS_KEY, MENSUAL_PLANNED_TRAINS_KEY,
             MENSUAL_DELAYED_DEPARTURE_TRAINS_KEY, MENSUAL_DELAYED_ARRIVAL_TRAINS_KEY]]
    
    # Datetime format into year and month columns for periods selection
    df["Date"]= pd.to_datetime(df["Date"])
    df.insert(0, "month", df["Date"].dt.month)
    df.insert(0, "year", df["Date"].dt.year)
    df = df.drop("Date", axis=1)
    
    return df


def init() -> None:
    """Initialization function to make global input csv dataframe"""
    global df
    df = load_csv_df()

def get_unique_city_pairs_list() -> list:
    """Retrieve unique pairs "departure-arrival" monitored by SNCF, 
    duplicates are dropped

    Returns:
        list: _description_
    """
    railway_cities = df[[DEPARTURE_STATION_KEY, ARRIVAL_STATION_KEY]]
    unique_railway_cities = railway_cities.value_counts().index.to_list()
    return unique_railway_cities


def get_reachable_destinations_list_from_city(departure: str) -> list:
    """Retrieve the list of destinations available from the departure railstation

    Returns:
        list: _description_
    """
    reachable_destinations = []
    city_pairs = get_unique_city_pairs_list()
    reachable_destinations = list(
        set(
            itertools.chain(
                *[city_pair for city_pair in city_pairs if departure in city_pair]
            )
        )
    )
    # one doesn't need to go directly to the place he came from, unless he needs an alibi...
    reachable_destinations.remove(departure)

    return reachable_destinations


def get_unique_railstations_df() -> pd.DataFrame:
    """Gets a dataframe list of all the departure stations of the country

    Returns:
        pd.DataFrame: Departure stations dataframe
    """
    unique_railstations = list(df[DEPARTURE_STATION_KEY].unique())
    return unique_railstations


# def file_upload() -> pd.DataFrame:
#     """Affiche la barre latérale avec les modules choisis

#     Returns:
#         pd.Dataframe: le dataframe contenant les données importées
#     """

#     file_uploader = st.sidebar.file_uploader(
#         "Charger un CSV (colonnes: Gares, Retards ...)", type=["csv"]
#     )

#     # Si l'utilisateur ne charge rien, on utilise le CSV d'exemple fourni
#     if file_uploader is not None:
#         df = load_csv_df(file_uploader)
#     else:
#         df = load_csv_df("data/raw/regularite-mensuelle-tgv-aqst.csv")
#         st.sidebar.info(
#             "Aucun fichier chargé : utilisation de `regularite-mensuelle-tgv-aqst.csv`."
#         )

#     st.sidebar.write(f"**{len(df)}** données chargées")

#     return df


def get_mean_departure_delay_df(departure_city: str) -> pd.DataFrame:
    """Returns the list of the mean delays of a departure city

    Args:
        departure_city (str): Departure city

    Returns:
        pd.DataFrame: Mean delays of a departure city
    """

    return df.loc[df[DEPARTURE_STATION_KEY] == departure_city][MEAN_DEPARTURE_DELAY_KEY]

def get_filtered_metrics_df(metrics: np.array, 
                            data_df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Returns a dataframe containing the selected metrics list

    Args:
        metrics (np.array): list of metrics to be filtered
        data_df (pd.DataFrame): input dataframe that contains the target metrics

    Returns:
        pd.DataFrame: filtered dataframe with only the listed metrics
    """
    if data_df is None:
        data_df = df
        
    return data_df[metrics]
 
def get_filtered_departure_arrival_stations_df(departure_station: str, 
                                              arrival_station: str, 
                                              data_df: pd.DataFrame | None = None
                                              ) -> pd.DataFrame:
    """Filters the input after the selected departure and arrival stations

    Args:
        departure_station (str): departure station
        arrival_station (str): arrival station
        data_df (np.array): input dataframe with DEPARTURE_STATION 
        and ARRIVAL_STATION columns

    Returns:
        pd.DataFrame: Filtered dataframe from selected departure and arrival stations
    """
    if data_df is None:
        data_df = df
        
    return data_df[(data_df[DEPARTURE_STATION_KEY] == departure_station) 
                   & (data_df[ARRIVAL_STATION_KEY] == arrival_station)]
    
def get_filtered_period_df(start_month: int, 
                           end_month: int, 
                           years_list: np.array, 
                           data_df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Filters the input dataframe after a given period of year and months

    Args:
        start_month (int): start month of period
        end_month (int): end month of period
        years_list (np.array): selected years list
        data_df (np.array): input dataframe with MONTH and YEAR columns

    Returns:
        pd.DataFrame: filtered dataframe with selected years and months
    """
    if data_df is None:
        data_df = df
        
    return data_df[(data_df[MONTH_KEY].isin(range(start_month, end_month + 1))) 
                   & (data_df[YEAR_KEY].isin(years_list))]