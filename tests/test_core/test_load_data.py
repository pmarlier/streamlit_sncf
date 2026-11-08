"""Data loading module tests with a small mocked dataframe."""

import datetime as dt
import itertools
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import streamlit as st

import core.load_data as load_data
from core import data_preprocessing as pr
from core import load_data as ld
from core.load_data import (
    get_directional_city_pairs_list,
    get_reachable_destinations_list_from_city,
    get_unique_city_pairs_list,
    get_unique_railstations_df,
)

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
MONTHLY_EXTERNAL_CAUSE_DELAY_PERCENT = "Prct retard pour causes externes"
MONTHLY_INFRASTRUCTURAL_CAUSE_DELAY_PERCENT = "Prct retard pour cause infrastructure"
MONTHLY_TRAFFIC_MANAGEMENT_CAUSE_DELAY_PERCENT = "Prct retard pour cause gestion trafic"
MONTHLY_MOBILE_EQUIPMENT_CAUSE_DELAY_PERCENT = "Prct retard pour cause matériel roulant"
MONTHLY_RAILSTATION_MANAGEMENT_CAUSE_DELAY_PERCENT = (
    "Prct retard pour cause gestion en gare et réutilisation de matériel"
)
MONTHLY_TRAVELER_CAUSE_DELAY_PERCENT = "Prct retard pour cause prise en compte voyageurs (affluence, gestions PSH, correspondances)"
MONTHLY_UNKNOWN_CAUSE_DELAY_PERCENT = "Prct retard causes non renseignées"

ARRIVAL_DELAY_COMMENT_KEY = "Commentaire retards à l'arrivée"
DEPARTURE_DELAY_COMMENT_KEY = "Commentaire retards au départ"
SERVICE_KEY = "Service"


def test_load_csv_df() -> pd.DataFrame:

    cols_to_be_dropped = [
        ARRIVAL_DELAY_COMMENT_KEY,
        DEPARTURE_DELAY_COMMENT_KEY,
        SERVICE_KEY,
    ]

    cols_to_be_kept = [
        DATE_KEY,
        DEPARTURE_STATION_KEY,
        ARRIVAL_STATION_KEY,
        MEAN_DEPARTURE_DELAY_KEY,
        MEAN_ARRIVAL_DELAY_KEY,
        MONTHLY_CANCELLED_TRAINS_KEY,
        MONTHLY_PLANNED_TRAINS_KEY,
        MONTHLY_DELAYED_DEPARTURE_TRAINS_KEY,
        MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY,
    ]

    df = pd.read_csv(CSV_PATH, sep=";")
    df = pr.preprocess_data(df)

    # Extract of columns to be dropped from the base dataframe, before filtering
    assert all(cdrop in df.columns for cdrop in cols_to_be_dropped)

    # Columns to be kept in the dataframe
    df = df[cols_to_be_kept]

    assert all(ckeep in df.columns for ckeep in cols_to_be_kept)
    assert all(cdrop not in df.columns for cdrop in cols_to_be_dropped)

    # Datetime format into year and month columns for periods selection
    df[DATE_KEY] = pd.to_datetime(df[DATE_KEY])

    df.insert(0, MONTH_KEY, df[DATE_KEY].dt.month)
    df.insert(0, YEAR_KEY, df[DATE_KEY].dt.year)
    df = df.drop(DATE_KEY, axis=1)
    years = sorted(df.year.unique())

    assert pd.api.types.is_integer_dtype(df[MONTH_KEY])
    assert pd.api.types.is_integer_dtype(df[YEAR_KEY])
    assert all(m in range(1, 13) for m in df[MONTH_KEY])
    assert all(y in years for y in df[YEAR_KEY])

    assert DATE_KEY not in df.columns


def test_init() -> None:
    """
    Test that all selected columns are imported.
    """
    cols_to_be_kept = [
        MONTH_KEY,
        YEAR_KEY,
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

    ld.init()

    assert type(ld.df) is pd.DataFrame
    assert all(col in cols_to_be_kept for col in ld.df.columns)


def test_get_directional_city_pairs_list(mocked_df):
    """
    Test must returns all unique (departure, arrival).
    The (arrival, departure) pair is different, so appear in the list
    """
    # initialize load_data module with mocked dataframe
    ld.set_monthly_punctuality_rate_df(mocked_df)

    result = get_directional_city_pairs_list()
    expected = [
        ("PARIS MONTPARNASSE", "RENNES"),
        ("RENNES", "PARIS MONTPARNASSE"),
        ("PARIS MONTPARNASSE", "BORDEAUX ST JEAN"),
        ("BORDEAUX ST JEAN", "PARIS MONTPARNASSE"),
        ("PARIS MONTPARNASSE", "NANTES"),
        ("NANTES", "PARIS MONTPARNASSE"),
    ]
    assert result == expected


def test_get_unique_city_pairs_list(mocked_df):
    """
    Test must returns unique couple of cities
    This time, (departure, arrival) and (arrival, departure) are considered duplicates
    One is dropped, and the list is sorted by alphabetical order
    """
    # initialize load_data module with mocked dataframe
    ld.set_monthly_punctuality_rate_df(mocked_df)

    result = get_unique_city_pairs_list()

    expected = [
        ("BORDEAUX ST JEAN", "PARIS MONTPARNASSE"),
        ("NANTES", "PARIS MONTPARNASSE"),
        ("PARIS MONTPARNASSE", "RENNES"),
    ]
    assert result == expected


def test_get_reachable_destinations_list_from_city(mocked_df):
    """
    Test reachable destinations from a city.
    """
    # initialize load_data module with mocked dataframe
    ld.set_monthly_punctuality_rate_df(mocked_df)

    # From Paris Montparnasse in the mock data
    result_paris = get_reachable_destinations_list_from_city("PARIS MONTPARNASSE")
    assert result_paris == ["BORDEAUX ST JEAN", "NANTES", "RENNES"]


def test_get_unique_railstations_df(mocked_df):
    """
    Test must returns a sorted list of unique rail stations.
    """
    # initialize load_data module with mocked dataframe
    ld.set_monthly_punctuality_rate_df(mocked_df)

    result = get_unique_railstations_df()
    assert result == ["BORDEAUX ST JEAN", "NANTES", "PARIS MONTPARNASSE", "RENNES"]


def test_get_filtered_metrics_df(mocked_df: pd.DataFrame) -> None:
    """Test the Pandas DataFrame column filter for a specific list of features

    Args:
        mocked_df (pd.DataFrame): The fake Pandas DataFrame if needed
    """
    # initialize load_data module with mocked dataframe
    ld.set_monthly_punctuality_rate_df(mocked_df)

    test_metrics = [MONTH_KEY, YEAR_KEY]

    result = ld.get_filtered_metrics_df(test_metrics, None)
    assert all(metric in result.columns for metric in test_metrics)

    result = ld.get_filtered_metrics_df(test_metrics, mocked_df)

    assert all(metric in result.columns for metric in test_metrics)


def test_get_filtered_departure_arrival_stations_df(
    mocked_df: pd.DataFrame,
) -> None:
    """Test the Pandas DataFrame row filter for a specific (departure arrival) couple

    Args:
        mocked_df (pd.DataFrame): The fake Pandas DataFrame if needed
    """
    # initialize load_data module with mocked dataframe
    ld.set_monthly_punctuality_rate_df(mocked_df)

    result = ld.get_filtered_departure_arrival_stations_df(
        "PARIS MONTPARNASSE", "RENNES", None
    )

    assert result[DEPARTURE_STATION_KEY].isin(["PARIS MONTPARNASSE"]).all()
    assert result[ARRIVAL_STATION_KEY].isin(["RENNES"]).all()

    result = ld.get_filtered_departure_arrival_stations_df(
        "PARIS MONTPARNASSE", "RENNES", mocked_df
    )

    assert result[DEPARTURE_STATION_KEY].isin(["PARIS MONTPARNASSE"]).all()
    assert result[ARRIVAL_STATION_KEY].isin(["RENNES"]).all()


def test_get_mean_departure_delay_df() -> None:
    # TODO : write a real test
    assert isinstance(ld.get_mean_departure_delay_df("toulon"), pd.Series)


def test_get_filtered_period_df(
    mocked_df: pd.DataFrame,
) -> None:
    """Test the Pandas DataFrame row filter for a specific time frame

    Args:
        mocked_df (pd.DataFrame): The fake Pandas DataFrame if needed
    """
    # initialize load_data module with mocked dataframe
    ld.set_monthly_punctuality_rate_df(mocked_df)

    result = ld.get_filtered_period_df(2, 12, [2018, 2020], None)
    assert result[YEAR_KEY].isin([2018, 2020]).all()
    assert result[MONTH_KEY].isin(np.arange(2, 13)).all()

    result = ld.get_filtered_period_df(2, 12, [2018, 2020], mocked_df)
    assert result[YEAR_KEY].isin([2018, 2020]).all()
    assert result[MONTH_KEY].isin(np.arange(2, 13)).all()
