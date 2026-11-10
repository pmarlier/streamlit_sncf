"""Data loading module"""

import itertools
import logging
import logging.config

import numpy as np
import pandas as pd
import streamlit as st

from core.data_preprocessing import preprocess_data

CSV_PATH = "./data/raw/regularite-mensuelle-tgv-aqst.csv"

# to simplify access to the column, keys are made up to avoid typing endless column name
DATE_KEY = "Date"
MONTH_KEY = "month"
YEAR_KEY = "year"
DEPARTURE_STATION_KEY = "Gare de départ"
ARRIVAL_STATION_KEY = "Gare d'arrivée"
MEAN_DEPARTURE_DELAY_KEY = "Retard moyen des trains en retard au départ"
MEAN_ARRIVAL_DELAY_KEY = "Retard moyen des trains en retard à l'arrivée"
MONTHLY_CANCELLED_TRAINS_KEY = "Nombre de trains annulés"
MONTHLY_PLANNED_TRAINS_KEY = "Nombre de circulations prévues"
MONTHLY_DELAYED_DEPARTURE_TRAINS_KEY = "Nombre de trains en retard au départ"
MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY = "Nombre de trains en retard à l'arrivée"
MONTHLY_EXTERNAL_CAUSE_DELAY_PERCENT = "Prct retard pour causes externes"
MONTHLY_INFRASTRUCTURAL_CAUSE_DELAY_PERCENT = "Prct retard pour cause infrastructure"
MONTHLY_TRAFFIC_MANAGEMENT_CAUSE_DELAY_PERCENT = "Prct retard pour cause gestion trafic"
MONTHLY_MOBILE_EQUIPMENT_CAUSE_DELAY_PERCENT = "Prct retard pour cause matériel roulant"
MONTHLY_RAILSTATION_MANAGEMENT_CAUSE_DELAY_PERCENT = (
    "Prct retard pour cause gestion en gare et réutilisation de matériel"
)
MONTHLY_TRAVELER_CAUSE_DELAY_PERCENT = "Prct retard pour cause prise en compte voyageurs (affluence, gestions PSH, correspondances)"
MONTHLY_UNKNOWN_CAUSE_DELAY_PERCENT = "Prct retard causes non renseignées"


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

    if df is not None:
        logger.debug(
            'Fichier "regularite-mensuelle-tgv-aqst".csv lu et converti en DataFrame'
        )
        df = preprocess_data(df)
        logger.debug("Prétraitement des données terminé")

        df = df[
            [
                DATE_KEY,
                DEPARTURE_STATION_KEY,
                ARRIVAL_STATION_KEY,
                MEAN_DEPARTURE_DELAY_KEY,
                MEAN_ARRIVAL_DELAY_KEY,
                MONTHLY_CANCELLED_TRAINS_KEY,
                MONTHLY_PLANNED_TRAINS_KEY,
                MONTHLY_DELAYED_DEPARTURE_TRAINS_KEY,
                MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY,
                MONTHLY_EXTERNAL_CAUSE_DELAY_PERCENT,
                MONTHLY_INFRASTRUCTURAL_CAUSE_DELAY_PERCENT,
                MONTHLY_TRAFFIC_MANAGEMENT_CAUSE_DELAY_PERCENT,
                MONTHLY_MOBILE_EQUIPMENT_CAUSE_DELAY_PERCENT,
                MONTHLY_RAILSTATION_MANAGEMENT_CAUSE_DELAY_PERCENT,
                MONTHLY_TRAVELER_CAUSE_DELAY_PERCENT,
                MONTHLY_UNKNOWN_CAUSE_DELAY_PERCENT,
            ]
        ]
        logger.debug("Filtrage des données terminé")
        logger.debug(
            "Seules les colonnes utiles sont chargées depuis le CSV (comportement nominal)"
        )

        # Datetime format into year and month columns for periods selection
        df[DATE_KEY] = pd.to_datetime(df[DATE_KEY])
        df.insert(0, MONTH_KEY, df[DATE_KEY].dt.month)
        df.insert(0, YEAR_KEY, df[DATE_KEY].dt.year)
        # df = df.drop(DATE_KEY, axis=1)

    return df


def get_monthly_stats_df() -> pd.DataFrame:
    """Initialization function to make global input csv dataframe"""
    # "global" is set for a variable to be used widely within a module
    return df


def set_monthly_stats_df(dataframe: pd.DataFrame):
    """Initialization function to make global input csv dataframe"""
    # "global" is set for a variable to be used widely within a module
    global df
    df = dataframe
    logger.debug("Dataframe chargé")


def init() -> None:
    """
    Initialization function to load CSV and
    set global variable to access dataframe
    """
    global logger
    logging.config.fileConfig("config/logging.conf")
    logger = logging.getLogger(__name__)
    set_monthly_stats_df(load_csv_df())


def get_directional_city_pairs_list() -> list:
    """Retrieve pairs "departure-arrival" monitored by SNCF,
    duplicates are dropped but same pairs in different direction are kept
    "departure-arrival" is different from "arrival_departure"

    Returns:
        list: _description_
    """
    railway_cities = df[[DEPARTURE_STATION_KEY, ARRIVAL_STATION_KEY]]
    directional_railway_cities = railway_cities.value_counts().index.to_list()

    return directional_railway_cities


def get_unique_city_pairs_list() -> list:
    """Retrieve unique pairs "departure-arrival" monitored by SNCF,
    duplicates and combinations "departure-arrival" and "arrival-departure" are dropped

    Returns:
        list: sorted alphabetically list of unique railstation couple,
    """
    city_pairs = get_directional_city_pairs_list()
    ordered_unique_city_pairs = list(sorted([(x, y) for y, x in city_pairs if x < y]))

    return ordered_unique_city_pairs


def get_reachable_destinations_list_from_city(departure: str) -> list:
    """Retrieve the list of destinations available from the departure railstation

    Returns:
        list: _description_
    """
    reachable_destinations = []
    city_pairs = get_directional_city_pairs_list()
    reachable_destinations = list(
        set(
            itertools.chain(
                *[city_pair for city_pair in city_pairs if departure in city_pair]
            )
        )
    )
    if departure in reachable_destinations:
        # no one need to go directly to the place he came from, unless he needs an alibi
        reachable_destinations.remove(departure)
    reachable_destinations = sorted(reachable_destinations)

    return reachable_destinations


def get_unique_railstations_df() -> pd.DataFrame:
    """Gets a dataframe list of all the departure stations of the country

    Returns:
        pd.DataFrame: Departure stations dataframe
    """
    unique_railstations = sorted(list(df[DEPARTURE_STATION_KEY].unique()))

    return unique_railstations


def get_mean_departure_delay_df(departure_city: str) -> pd.DataFrame:
    """Returns the list of the mean delays of a departure city

    Args:
        departure_city (str): Departure city

    Returns:
        pd.DataFrame: Mean delays of a departure city
    """

    return df.loc[df[DEPARTURE_STATION_KEY] == departure_city][MEAN_DEPARTURE_DELAY_KEY]


def get_filtered_metrics_df(
    metrics: np.array, data_df: pd.DataFrame | None = None
) -> pd.DataFrame:
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


def get_filtered_departure_arrival_stations_df(
    departure_station: str, arrival_station: str, data_df: pd.DataFrame | None = None
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

    return data_df[
        (data_df[DEPARTURE_STATION_KEY] == departure_station)
        & (data_df[ARRIVAL_STATION_KEY] == arrival_station)
    ]


def get_filtered_period_df(
    start_month: int,
    end_month: int,
    years_list: np.array,
    data_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
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

    return data_df[
        (data_df[MONTH_KEY].isin(range(start_month, end_month + 1)))
        & (data_df[YEAR_KEY].isin(years_list))
    ]
