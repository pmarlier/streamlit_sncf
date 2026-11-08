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

    global df
    df = ld.load_csv_df()

    assert type(df) is pd.DataFrame
    assert all(col in cols_to_be_kept for col in df.columns)


def test_get_directional_city_pairs_list():
    """
    Test that get_directional_city_pairs_list returns all unique (departure, arrival).
    """

    result = get_directional_city_pairs_list()
    expected = [
        ("MACON LOCHE", "PARIS LYON"),
        ("MARSEILLE ST CHARLES", "LYON PART DIEU"),
        ("DIJON VILLE", "PARIS LYON"),
        ("PARIS LYON", "CHAMBERY CHALLES LES EAUX"),
        ("PARIS LYON", "BELLEGARDE (AIN)"),
        ("PARIS EST", "STRASBOURG"),
        ("STRASBOURG", "PARIS EST"),
        ("MULHOUSE VILLE", "PARIS LYON"),
        ("PARIS LYON", "DIJON VILLE"),
        ("PARIS LYON", "MULHOUSE VILLE"),
        ("BELLEGARDE (AIN)", "PARIS LYON"),
        ("CHAMBERY CHALLES LES EAUX", "PARIS LYON"),
        ("LYON PART DIEU", "MARSEILLE ST CHARLES"),
        ("PARIS LYON", "MACON LOCHE"),
        ("BORDEAUX ST JEAN", "PARIS MONTPARNASSE"),
        ("LE MANS", "PARIS MONTPARNASSE"),
        ("PARIS MONTPARNASSE", "LA ROCHELLE VILLE"),
        ("PARIS MONTPARNASSE", "NANTES"),
        ("POITIERS", "PARIS MONTPARNASSE"),
        ("ST MALO", "PARIS MONTPARNASSE"),
        ("TOULOUSE MATABIAU", "PARIS MONTPARNASSE"),
        ("VANNES", "PARIS MONTPARNASSE"),
        ("REIMS", "PARIS EST"),
        ("DOUAI", "PARIS NORD"),
        ("LILLE", "PARIS NORD"),
        ("LILLE", "MARSEILLE ST CHARLES"),
        ("PARIS NORD", "DUNKERQUE"),
        ("AIX EN PROVENCE TGV", "PARIS LYON"),
        ("ANNECY", "PARIS LYON"),
        ("GRENOBLE", "PARIS LYON"),
        ("LYON PART DIEU", "MARNE LA VALLEE"),
        ("MONTPELLIER", "PARIS LYON"),
        ("PARIS LYON", "MARSEILLE ST CHARLES"),
        ("BARCELONA", "PARIS LYON"),
        ("FRANCFORT", "PARIS EST"),
        ("PARIS LYON", "LAUSANNE"),
        ("PARIS MONTPARNASSE", "LAVAL"),
        ("PARIS MONTPARNASSE", "VANNES"),
        ("ST PIERRE DES CORPS", "PARIS MONTPARNASSE"),
        ("TOURS", "PARIS MONTPARNASSE"),
        ("PARIS EST", "METZ"),
        ("LYON PART DIEU", "LILLE"),
        ("PARIS NORD", "DOUAI"),
        ("BESANCON FRANCHE COMTE TGV", "PARIS LYON"),
        ("MARSEILLE ST CHARLES", "PARIS LYON"),
        ("PARIS LYON", "AVIGNON TGV"),
        ("PARIS LYON", "BESANCON FRANCHE COMTE TGV"),
        ("PARIS LYON", "PERPIGNAN"),
        ("PERPIGNAN", "PARIS LYON"),
        ("VALENCE ALIXAN TGV", "PARIS LYON"),
        ("STUTTGART", "PARIS EST"),
        ("LYON PART DIEU", "RENNES"),
        ("PARIS MONTPARNASSE", "ANGERS SAINT LAUD"),
        ("PARIS MONTPARNASSE", "ANGOULEME"),
        ("PARIS MONTPARNASSE", "BREST"),
        ("PARIS MONTPARNASSE", "QUIMPER"),
        ("PARIS MONTPARNASSE", "ST PIERRE DES CORPS"),
        ("PARIS MONTPARNASSE", "TOURS"),
        ("RENNES", "PARIS MONTPARNASSE"),
        ("METZ", "PARIS EST"),
        ("NANCY", "PARIS EST"),
        ("NANTES", "STRASBOURG"),
        ("PARIS EST", "REIMS"),
        ("LILLE", "LYON PART DIEU"),
        ("PARIS NORD", "LILLE"),
        ("LE CREUSOT MONTCEAU MONTCHANIN", "PARIS LYON"),
        ("MARNE LA VALLEE", "LYON PART DIEU"),
        ("NICE VILLE", "PARIS LYON"),
        ("PARIS LYON", "GRENOBLE"),
        ("PARIS LYON", "MONTPELLIER"),
        ("PARIS LYON", "NICE VILLE"),
        ("LAUSANNE", "PARIS LYON"),
        ("PARIS LYON", "BARCELONA"),
        ("ANGOULEME", "PARIS MONTPARNASSE"),
        ("BREST", "PARIS MONTPARNASSE"),
        ("LA ROCHELLE VILLE", "PARIS MONTPARNASSE"),
        ("NANTES", "PARIS MONTPARNASSE"),
        ("PARIS MONTPARNASSE", "BORDEAUX ST JEAN"),
        ("PARIS MONTPARNASSE", "RENNES"),
        ("PARIS MONTPARNASSE", "ST MALO"),
        ("PARIS MONTPARNASSE", "TOULOUSE MATABIAU"),
        ("QUIMPER", "PARIS MONTPARNASSE"),
        ("RENNES", "LYON PART DIEU"),
        ("MARSEILLE ST CHARLES", "LILLE"),
        ("AVIGNON TGV", "PARIS LYON"),
        ("LYON PART DIEU", "PARIS LYON"),
        ("LYON PART DIEU", "MONTPELLIER"),
        ("MONTPELLIER", "LYON PART DIEU"),
        ("PARIS LYON", "NIMES"),
        ("PARIS LYON", "VALENCE ALIXAN TGV"),
        ("SAINT ETIENNE CHATEAUCREUX", "PARIS LYON"),
        ("GENEVE", "PARIS LYON"),
        ("PARIS EST", "STUTTGART"),
        ("ANGERS SAINT LAUD", "PARIS MONTPARNASSE"),
        ("LAVAL", "PARIS MONTPARNASSE"),
        ("PARIS MONTPARNASSE", "LE MANS"),
        ("PARIS MONTPARNASSE", "POITIERS"),
        ("PARIS EST", "NANCY"),
        ("STRASBOURG", "NANTES"),
        ("ARRAS", "PARIS NORD"),
        ("DUNKERQUE", "PARIS NORD"),
        ("PARIS NORD", "ARRAS"),
        ("MARNE LA VALLEE", "MARSEILLE ST CHARLES"),
        ("MARSEILLE ST CHARLES", "MARNE LA VALLEE"),
        ("NIMES", "PARIS LYON"),
        ("PARIS LYON", "AIX EN PROVENCE TGV"),
        ("PARIS LYON", "ANNECY"),
        ("PARIS LYON", "LE CREUSOT MONTCEAU MONTCHANIN"),
        ("PARIS LYON", "LYON PART DIEU"),
        ("PARIS LYON", "SAINT ETIENNE CHATEAUCREUX"),
        ("PARIS LYON", "TOULON"),
        ("TOULON", "PARIS LYON"),
        ("PARIS EST", "FRANCFORT"),
        ("PARIS LYON", "GENEVE"),
        ("PARIS LYON", "ZURICH"),
        ("MARSEILLE ST CHARLES", "TOURCOING"),
        ("ZURICH", "PARIS LYON"),
        ("BORDEAUX ST JEAN", "TOURCOING"),
        ("TOURCOING", "BORDEAUX ST JEAN"),
        ("PARIS LYON", "ITALIE"),
        ("ITALIE", "PARIS LYON"),
        ("MADRID", "MARSEILLE ST CHARLES"),
        ("MARSEILLE ST CHARLES", "MADRID"),
        ("TOURCOING", "MARSEILLE ST CHARLES"),
        ("PARIS VAUGIRARD", "BORDEAUX ST JEAN"),
        ("PARIS VAUGIRARD", "NANTES"),
        ("RENNES", "PARIS VAUGIRARD"),
        ("NANTES", "PARIS VAUGIRARD"),
        ("BORDEAUX ST JEAN", "PARIS VAUGIRARD"),
        ("PARIS VAUGIRARD", "RENNES"),
    ]
    assert result == expected


def test_get_unique_city_pairs_list():

    result = get_unique_city_pairs_list()
    # Based on the specific logic in load_data.py:
    # only pairs (x, y) where (y, x) exists AND x < y
    expected = [
        ("AIX EN PROVENCE TGV", "PARIS LYON"),
        ("ANGERS SAINT LAUD", "PARIS MONTPARNASSE"),
        ("ANGOULEME", "PARIS MONTPARNASSE"),
        ("ANNECY", "PARIS LYON"),
        ("ARRAS", "PARIS NORD"),
        ("AVIGNON TGV", "PARIS LYON"),
        ("BARCELONA", "PARIS LYON"),
        ("BELLEGARDE (AIN)", "PARIS LYON"),
        ("BESANCON FRANCHE COMTE TGV", "PARIS LYON"),
        ("BORDEAUX ST JEAN", "PARIS MONTPARNASSE"),
        ("BORDEAUX ST JEAN", "PARIS VAUGIRARD"),
        ("BORDEAUX ST JEAN", "TOURCOING"),
        ("BREST", "PARIS MONTPARNASSE"),
        ("CHAMBERY CHALLES LES EAUX", "PARIS LYON"),
        ("DIJON VILLE", "PARIS LYON"),
        ("DOUAI", "PARIS NORD"),
        ("DUNKERQUE", "PARIS NORD"),
        ("FRANCFORT", "PARIS EST"),
        ("GENEVE", "PARIS LYON"),
        ("GRENOBLE", "PARIS LYON"),
        ("ITALIE", "PARIS LYON"),
        ("LA ROCHELLE VILLE", "PARIS MONTPARNASSE"),
        ("LAUSANNE", "PARIS LYON"),
        ("LAVAL", "PARIS MONTPARNASSE"),
        ("LE CREUSOT MONTCEAU MONTCHANIN", "PARIS LYON"),
        ("LE MANS", "PARIS MONTPARNASSE"),
        ("LILLE", "LYON PART DIEU"),
        ("LILLE", "MARSEILLE ST CHARLES"),
        ("LILLE", "PARIS NORD"),
        ("LYON PART DIEU", "MARNE LA VALLEE"),
        ("LYON PART DIEU", "MARSEILLE ST CHARLES"),
        ("LYON PART DIEU", "MONTPELLIER"),
        ("LYON PART DIEU", "PARIS LYON"),
        ("LYON PART DIEU", "RENNES"),
        ("MACON LOCHE", "PARIS LYON"),
        ("MADRID", "MARSEILLE ST CHARLES"),
        ("MARNE LA VALLEE", "MARSEILLE ST CHARLES"),
        ("MARSEILLE ST CHARLES", "PARIS LYON"),
        ("MARSEILLE ST CHARLES", "TOURCOING"),
        ("METZ", "PARIS EST"),
        ("MONTPELLIER", "PARIS LYON"),
        ("MULHOUSE VILLE", "PARIS LYON"),
        ("NANCY", "PARIS EST"),
        ("NANTES", "PARIS MONTPARNASSE"),
        ("NANTES", "PARIS VAUGIRARD"),
        ("NANTES", "STRASBOURG"),
        ("NICE VILLE", "PARIS LYON"),
        ("NIMES", "PARIS LYON"),
        ("PARIS EST", "REIMS"),
        ("PARIS EST", "STRASBOURG"),
        ("PARIS EST", "STUTTGART"),
        ("PARIS LYON", "PERPIGNAN"),
        ("PARIS LYON", "SAINT ETIENNE CHATEAUCREUX"),
        ("PARIS LYON", "TOULON"),
        ("PARIS LYON", "VALENCE ALIXAN TGV"),
        ("PARIS LYON", "ZURICH"),
        ("PARIS MONTPARNASSE", "POITIERS"),
        ("PARIS MONTPARNASSE", "QUIMPER"),
        ("PARIS MONTPARNASSE", "RENNES"),
        ("PARIS MONTPARNASSE", "ST MALO"),
        ("PARIS MONTPARNASSE", "ST PIERRE DES CORPS"),
        ("PARIS MONTPARNASSE", "TOULOUSE MATABIAU"),
        ("PARIS MONTPARNASSE", "TOURS"),
        ("PARIS MONTPARNASSE", "VANNES"),
        ("PARIS VAUGIRARD", "RENNES"),
    ]
    assert result == expected


def test_get_reachable_destinations_list_from_city():
    """
    Test reachable destinations from a city.
    """
    # From Paris
    result_paris = get_reachable_destinations_list_from_city("PARIS LYON")
    assert result_paris == [
        "AIX EN PROVENCE TGV",
        "ANNECY",
        "AVIGNON TGV",
        "BARCELONA",
        "BELLEGARDE (AIN)",
        "BESANCON FRANCHE COMTE TGV",
        "CHAMBERY CHALLES LES EAUX",
        "DIJON VILLE",
        "GENEVE",
        "GRENOBLE",
        "ITALIE",
        "LAUSANNE",
        "LE CREUSOT MONTCEAU MONTCHANIN",
        "LYON PART DIEU",
        "MACON LOCHE",
        "MARSEILLE ST CHARLES",
        "MONTPELLIER",
        "MULHOUSE VILLE",
        "NICE VILLE",
        "NIMES",
        "PERPIGNAN",
        "SAINT ETIENNE CHATEAUCREUX",
        "TOULON",
        "VALENCE ALIXAN TGV",
        "ZURICH",
    ]

    # From Lyon
    # Pairs containing Lyon: (Paris, Lyon), (Lyon, Paris), (Lyon, Marseille)
    # Reachable: Paris, Marseille
    result_lyon = get_reachable_destinations_list_from_city("PARIS NORD")
    assert result_lyon == ["ARRAS", "DOUAI", "DUNKERQUE", "LILLE"]


def test_get_unique_railstations_df():
    """
    Test get_unique_railstations_df returns a sorted list of unique departure stations.
    """
    result = get_unique_railstations_df()
    assert result == [
        "AIX EN PROVENCE TGV",
        "ANGERS SAINT LAUD",
        "ANGOULEME",
        "ANNECY",
        "ARRAS",
        "AVIGNON TGV",
        "BARCELONA",
        "BELLEGARDE (AIN)",
        "BESANCON FRANCHE COMTE TGV",
        "BORDEAUX ST JEAN",
        "BREST",
        "CHAMBERY CHALLES LES EAUX",
        "DIJON VILLE",
        "DOUAI",
        "DUNKERQUE",
        "FRANCFORT",
        "GENEVE",
        "GRENOBLE",
        "ITALIE",
        "LA ROCHELLE VILLE",
        "LAUSANNE",
        "LAVAL",
        "LE CREUSOT MONTCEAU MONTCHANIN",
        "LE MANS",
        "LILLE",
        "LYON PART DIEU",
        "MACON LOCHE",
        "MADRID",
        "MARNE LA VALLEE",
        "MARSEILLE ST CHARLES",
        "METZ",
        "MONTPELLIER",
        "MULHOUSE VILLE",
        "NANCY",
        "NANTES",
        "NICE VILLE",
        "NIMES",
        "PARIS EST",
        "PARIS LYON",
        "PARIS MONTPARNASSE",
        "PARIS NORD",
        "PARIS VAUGIRARD",
        "PERPIGNAN",
        "POITIERS",
        "QUIMPER",
        "REIMS",
        "RENNES",
        "SAINT ETIENNE CHATEAUCREUX",
        "ST MALO",
        "ST PIERRE DES CORPS",
        "STRASBOURG",
        "STUTTGART",
        "TOULON",
        "TOULOUSE MATABIAU",
        "TOURCOING",
        "TOURS",
        "VALENCE ALIXAN TGV",
        "VANNES",
        "ZURICH",
    ]


def test_get_filtered_metrics_df(mocked_df: pd.DataFrame) -> None:
    """Test the Pandas DataFrame column filter for a specific list of features

    Args:
        mocked_df (pd.DataFrame): The fake Pandas DataFrame if needed
    """

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


def test_get_filtered_period_df(
    mocked_df: pd.DataFrame,
) -> None:
    """Test the Pandas DataFrame row filter for a specific time frame

    Args:
        mocked_df (pd.DataFrame): The fake Pandas DataFrame if needed
    """
    result = ld.get_filtered_period_df(2, 12, [2018, 2020], None)
    assert result[YEAR_KEY].isin([2018, 2020]).all()
    assert result[MONTH_KEY].isin(np.arange(2, 13)).all()

    result = ld.get_filtered_period_df(2, 12, [2018, 2020], mocked_df)
    assert result[YEAR_KEY].isin([2018, 2020]).all()
    assert result[MONTH_KEY].isin(np.arange(2, 13)).all()
