import pandas as pd
import pytest

from core.railway_data import railway_geo as rg
from core.railway_data import railway_network


def test_load_railway_geo_data(capfd) -> pd.DataFrame:
    """Test the loading of the csv file with railway geo data

    Args:
        capfd: the pytest fixture to capture stdout

    Returns:
        pd.DataFrame: the dataframe output loaded
    """
    # testing default configuration with no filepath given as argument
    railway_geo_df = rg.load_railway_geo_data()

    assert isinstance(railway_geo_df, pd.DataFrame)

    rg.load_railway_geo_data("fake_path_for_exception_test")

    out, err = capfd.readouterr()
    assert (
        out
        == "core.railway_data.railway_geo : FAIL Loading railway geo file at fake_path_for_exception_test\n"
    )


def test_load_railstation_geo_data(capfd) -> pd.DataFrame:
    """Test the loading of the csv file with railstation data

    Args:
        capfd: the pytest fixture to capture stdout

    Returns:
        pd.DataFrame: the dataframe output loaded
    """
    # testing default configuration with no filepath given as argument
    railstation_geo_df = rg.load_railstation_geo_data()

    assert isinstance(railstation_geo_df, pd.DataFrame)

    rg.load_railstation_geo_data("fake_path_for_exception_test")

    out, err = capfd.readouterr()
    assert (
        out
        == "core.railway_data.railway_geo : FAIL Loading railstation geo file at fake_path_for_exception_test\n"
    )


def test_init() -> None:
    """
    Test csv import
    """
    rg.init()
    # check that imported data are from the right class
    assert isinstance(rg.railway_geo_df, pd.DataFrame)
    assert isinstance(rg.railstation_geo_df, pd.DataFrame)


def test_set_railway_geo_df(mocked_railway_geo_df):
    """Mock for lignes-par-region-administrative.csv to draw precise railway
    Use mock data from conftest.py, between Paris and Rennes

    Paris-Montparnasse-Pasteur;48.83921287344567, 2.3181430216303696
    Rennes;48.10337713690151, 1.670824886184606

    """

    rg.set_railway_geo_df(None)
    assert rg.railway_geo_df is None

    rg.set_railway_geo_df(mocked_railway_geo_df)
    assert isinstance(rg.railway_geo_df, pd.DataFrame)


def test_set_railstation_geo_df(mocked_railstation_geo_df):
    """Mock for liste-des-gares.csv
    Sample of the real file, only for the used column

    ["LIBELLE"] ; ["Geo Point"]

    [...];LIBELLE;[...];Geo Point

    Paris-Montparnasse-Pasteur;48.83921287344567, 2.3181430216303696
    Rennes;48.10337713690151, -1.670824886184606

    """

    rg.set_railstation_geo_df(None)
    assert rg.railstation_geo_df is None

    rg.set_railstation_geo_df(mocked_railstation_geo_df)
    assert isinstance(rg.railstation_geo_df, pd.DataFrame)


def test_get_coords_for_city_pair(mocked_railstation_geo_df):
    """Mock for liste-des-gares.csv
    Sample of the real file, only for the used column

    ["LIBELLE"] ; ["Geo Point"]

    [...];LIBELLE;[...];Geo Point

    Paris-Montparnasse-Pasteur;48.83921287344567, 2.3181430216303696
    Rennes;48.10337713690151, -1.670824886184606

    """
    rg.set_railstation_geo_df(mocked_railstation_geo_df)

    departure_railstation_geo_point, arrival_railstation_geo_point = (
        rg.get_coords_for_city_pair("paris-montparnasse-pasteur", "rennes")
    )

    # check that results match with the mock data
    assert len(departure_railstation_geo_point) == 2
    assert departure_railstation_geo_point[0] == "48.8"
    assert departure_railstation_geo_point[1] == "2.3"

    assert len(arrival_railstation_geo_point) == 2
    assert arrival_railstation_geo_point[0] == "48.4"
    assert arrival_railstation_geo_point[1] == "1.6"


def test_get_railway_geo_point_by_id(
    mocked_railway_geo_df: pd.DataFrame, mocked_railstation_geo_df: pd.DataFrame
):
    """Mock for liste-des-gares.csv
    Sample of the real file, only for the used column

    ["LIBELLE"] ; ["Geo Point"]

    [...];LIBELLE;[...];Geo Point

    Paris-Montparnasse-Pasteur;48.83921287344567, 2.3181430216303696
    Rennes;48.10337713690151, -1.670824886184606

    """
    rg.set_railstation_geo_df(mocked_railstation_geo_df)
    rg.set_railway_geo_df(mocked_railway_geo_df)

    # perfect match between railway and departure and arrival railstations
    result = rg.get_railway_geo_point_by_id(101, "Paris-Montparnasse-Pasteur", "Rennes")
    assert result == [[(48.8, 2.3), (48.4, 1.6)]]

    # railway exceed departure railstation, just keep points between railstations
    result = rg.get_railway_geo_point_by_id(102, "Paris-Montparnasse-Pasteur", "Rennes")
    # only keep arrival
    assert result == [[(48.8, 2.3), (48.4, 1.6)]]

    # railway exceed arrival railstation
    result = rg.get_railway_geo_point_by_id(103, "Paris-Montparnasse-Pasteur", "Rennes")
    # only keep departure
    assert result == [[(48.8, 2.3)]]

    # railway has nothing to do with railstation
    result = rg.get_railway_geo_point_by_id(104, "Paris-Montparnasse-Pasteur", "Rennes")
    # no match
    assert result == []

    # empty line
    result = rg.get_railway_geo_point_by_id(105, "Paris-Montparnasse-Pasteur", "Rennes")
    assert result == []
