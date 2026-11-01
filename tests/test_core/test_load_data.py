"""Data loading module tests with a small mocked dataframe."""

import pandas as pd
import numpy as np
import streamlit as st
import itertools
import datetime as dt

from pathlib import Path
import pandas as pd
import pytest
from core import load_data as ld
from core import data_preprocessing as pr

CSV_PATH = "./data/raw/regularite-mensuelle-tgv-aqst.csv"

# to simplify access to the column, keys are made up to avoid typing endless column names
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

ARRIVAL_DELAY_COMMENT_KEY = "Commentaire retards à l'arrivée"
DEPARTURE_DELAY_COMMENT_KEY = "Commentaire retards au départ"
SERVICE_KEY = "Service"

def test_load_csv_df() -> pd.DataFrame:

    cols_to_be_dropped = [ARRIVAL_DELAY_COMMENT_KEY, 
                          DEPARTURE_DELAY_COMMENT_KEY, 
                          SERVICE_KEY]
    
    cols_to_be_kept = [DATE_KEY, DEPARTURE_STATION_KEY, ARRIVAL_STATION_KEY, 
             MEAN_DEPARTURE_DELAY_KEY, MEAN_ARRIVAL_DELAY_KEY, 
             MONTHLY_CANCELLED_TRAINS_KEY, MONTHLY_PLANNED_TRAINS_KEY,
             MONTHLY_DELAYED_DEPARTURE_TRAINS_KEY, MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY]
    
    
    df = pd.read_csv(CSV_PATH, sep=";")
    df = pr.preprocess_data(df)
    
    # Extract of columns to be dropped from the base dataframe, before filtering
    assert all(cdrop in df.columns for cdrop in cols_to_be_dropped)
    
    # Columns to be kept in the dataframe
    df = df[cols_to_be_kept]
    
    assert all(ckeep in df.columns for ckeep in cols_to_be_kept) 
    assert all(cdrop not in df.columns for cdrop in cols_to_be_dropped)
    
    # Datetime format into year and month columns for periods selection
    df[DATE_KEY]= pd.to_datetime(df[DATE_KEY])
    
    df.insert(0, MONTH_KEY, df[DATE_KEY].dt.month)
    df.insert(0, YEAR_KEY, df[DATE_KEY].dt.year)
    df = df.drop(DATE_KEY, axis=1)
    years = sorted(df.year.unique())

    assert pd.api.types.is_integer_dtype(df[MONTH_KEY])
    assert pd.api.types.is_integer_dtype(df[YEAR_KEY])
    assert all(m in range(1,13) for m in df[MONTH_KEY])
    assert all(y in years for y in df[YEAR_KEY])

    assert DATE_KEY not in df.columns


def test_init() -> None:
    cols_to_be_kept = [MONTH_KEY, YEAR_KEY, DEPARTURE_STATION_KEY, ARRIVAL_STATION_KEY, 
             MEAN_DEPARTURE_DELAY_KEY, MEAN_ARRIVAL_DELAY_KEY, 
             MONTHLY_CANCELLED_TRAINS_KEY, MONTHLY_PLANNED_TRAINS_KEY,
             MONTHLY_DELAYED_DEPARTURE_TRAINS_KEY, MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY]
    
    global df
    df = ld.load_csv_df()
    
    assert type(df) is pd.DataFrame
    assert all(col in cols_to_be_kept for col in df.columns)

# !! Tests to be written
def get_unique_city_pairs_list() -> list:
    """Retrieve unique pairs "departure-arrival" monitored by SNCF, 
    duplicates are dropped

    Returns:
        list: _description_
    """
    railway_cities = df[[DEPARTURE_STATION_KEY, ARRIVAL_STATION_KEY]]
    unique_railway_cities = railway_cities.value_counts().index.to_list()
    return unique_railway_cities

# !! Tests to be written
def get_reachable_destinations_list_from_city(departure: str) -> list:
    """Retrieve the list of destinations available from the departure railstation

    Returns:
        list: _description_
    """
    reachable_destinations = []
    city_pairs = get_unique_city_pairs_list()
    reachable_destinations = list(set(itertools.chain(*[city_pair 
                                                        for city_pair in city_pairs 
                                                        if departure in city_pair])))
    # one doesn't need to go directly to the place he came from, unless he needs an alibi... do you, PM ?
    reachable_destinations.remove(departure)

    return reachable_destinations

# !! Tests to be written
def get_unique_railstations_df() -> pd.DataFrame:
    """Gets a dataframe list of all the departure stations of the country

    Returns:
        pd.DataFrame: Departure stations dataframe
    """
    unique_railstations = list(df[DEPARTURE_STATION_KEY].unique())
    return unique_railstations


# def file_upload() -> pd.DataFrame:
    """Affiche la barre latérale avec les modules choisis

    Returns:
        pd.Dataframe: le dataframe contenant les données importées
    """

    file_uploader = st.sidebar.file_uploader(
        "Charger un CSV (colonnes: Gares, Retards ...)", type=["csv"]
    )

    # Si l'utilisateur ne charge rien, on utilise le CSV d'exemple fourni
    if file_uploader is not None:
        df = ld.load_csv_df(file_uploader)
    else:
        df = ld.load_csv_df("data/raw/regularite-mensuelle-tgv-aqst.csv")
        st.sidebar.info(
            "Aucun fichier chargé : utilisation de `regularite-mensuelle-tgv-aqst.csv`."
        )

    st.sidebar.write(f"**{len(df)}** données chargées")

    return df


# def get_mean_departure_delay_df(departure_city: str) -> pd.DataFrame:
#     """Returns the list of the mean delays of a departure city

#     Args:
#         departure_city (str): Departure city

#     Returns:
#         pd.DataFrame: Mean delays of a departure city
#     """

#     return df.loc[df[DEPARTURE_STATION_KEY] == departure_city][MEAN_DEPARTURE_DELAY_KEY]
    
def test_get_filtered_metrics_df(mocked_df: pd.DataFrame) -> None:
    test_metrics = [MONTH_KEY, YEAR_KEY]
    result = ld.get_filtered_metrics_df(
        test_metrics, mocked_df
    )
        
    assert all(metric in result.columns for metric in test_metrics)
 
def test_get_filtered_departure_arrival_stations_df(
    mocked_df: pd.DataFrame,
) -> None:
    result = ld.get_filtered_departure_arrival_stations_df(
        "PARIS MONTPARNASSE", "RENNES", mocked_df
    )

    assert result[DEPARTURE_STATION_KEY].isin(["PARIS MONTPARNASSE"]).all()
    assert result[ARRIVAL_STATION_KEY].isin(["RENNES"]).all()
    
def test_get_filtered_period_df(
    mocked_df: pd.DataFrame,
) -> None:
    result = ld.get_filtered_period_df(
        2, 12, [2018, 2020], mocked_df
    )
    assert result[YEAR_KEY].isin([2018, 2020]).all()
    assert result[MONTH_KEY].isin(np.arange(2, 13)).all()