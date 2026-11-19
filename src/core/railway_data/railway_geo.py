import json
import logging.config

import pandas as pd
from geopy import distance
from unidecode import unidecode

from core import railway_data

CSV_GEO_PATH = "./data/raw/lignes-par-region-administrative.csv"
CSV_RAILSTATIONS_PATH = "./data/raw/liste-des-gares.csv"


def load_railway_geo_data(filepath: str = CSV_GEO_PATH) -> pd.DataFrame:
    """Load geographical points dataframe from all the French railway network
    This dataframe is downloadable from the SNCF open data website
    It provides geographical coordinates for railway section of the network
    It also map these coordinates with railway identification number
    The format of the coordinates are reverse-stored regarding the lat/long convention
    This dataframe is combined with the railstation dataframe to rebuild the connection
    between railstations and the railway path

    Args:
        filepath (str, optional): The filepath of the csv file furnished by SNCF.
        Defaults to CSV_PATH.

    Returns:
        pd.DataFrame: Return the dataframe containing geo data points for railways
    """
    try:
        railway_geo_df = pd.read_table(filepath, delimiter=";")
    except Exception:
        logger.error(f"Fail Loading railway geo file at {filepath}")
        return None

    return railway_geo_df


def load_railstation_geo_data(filepath: str = CSV_RAILSTATIONS_PATH) -> pd.DataFrame:
    """Load geographical points dataframe from all the French railstations
    This dataframe is downloadable from the SNCF open data website
    It provides geographical coordinates for each railstation over the french territory
    It also map these cities with railway identification number for which the given
    railstation is a strating point. This dataframe is combined with the railway geo
    dataframe to rebuild the connection between railstations and the railway path

    Args:
        filepath (str, optional): The filepath of the csv file furnished by SNCF.
        Defaults to CSV_PATH.

    Returns:
        pd.DataFrame: Return the dataframe containing geo data points for railstations
    """
    try:
        railstation_geo_df = pd.read_table(filepath, delimiter=";")
        railstation_geo_df["LIBELLE"] = [
            unidecode(railway_station.lower().replace(" ", "-"))
            for railway_station in railstation_geo_df["LIBELLE"]
        ]
    except Exception:
        logger.error(f"Fail Loading railstation geo file at {filepath}")
        return None

    return railstation_geo_df


def set_railway_geo_df(dataframe: pd.DataFrame) -> None:
    """Setter for the dataframe containing railway geo dataframe

    Args:
        dataframe (pd.DataFrame): the dataframe containing the geographical
        coordinates of each railway section over the french railway network
    """
    global railway_geo_df
    railway_geo_df = dataframe
    logger.debug("Railway Geo Dataframe set")


def set_railstation_geo_df(dataframe: pd.DataFrame) -> None:
    """Setter for the dataframe containing railstations geo dataframe

    Args:
        dataframe (pd.DataFrame): the dataframe containing the geographical
        coordinates of each railstations over the french railway network
    """
    global railstation_geo_df
    railstation_geo_df = dataframe
    logger.debug("Railstation Geo Dataframe set")


def init() -> None:
    """Initialize logger and set dataframe imported from CSV files"""
    global logger
    logging.config.fileConfig("config/logging.conf")
    logger = logging.getLogger(__name__)
    set_railway_geo_df(load_railway_geo_data())
    set_railstation_geo_df(load_railstation_geo_data())
    logger.debug("Railway geo data initialization done")


def get_coords_for_city_pair(departure_city: str, arrival_city: str) -> list:
    """Retrieve couple (latitude, longitude) for both departure and arrival city pair
    Data are collected from the geo railstation dataframe

    Args:
        departure_city (str): the departure city of the railway link
        arrival_city (str): the arrival city of the railway link

    Returns:
        list: A list of two tuples built from geo point of both departure and
        arrival cities
        Each coordinates are stored under the classic format
        [latitude (N/S), longitude (E/W)]
    """
    departure_railstation_geo = railstation_geo_df[
        railstation_geo_df["LIBELLE"]
        == railway_data.get_processed_city_name(departure_city)
    ]
    arrival_railstation_geo = railstation_geo_df[
        railstation_geo_df["LIBELLE"]
        == railway_data.get_processed_city_name(arrival_city)
    ]

    departure_railstation_geo_point = (
        departure_railstation_geo["Geo Point"].values[0].split(", ")
    )
    arrival_railstation_geo_point = (
        arrival_railstation_geo["Geo Point"].values[0].split(", ")
    )

    logger.debug("Trip coordinates set ! ready to ride !")
    return departure_railstation_geo_point, arrival_railstation_geo_point


def get_railway_geo_point_by_id(
    railway_id: int, departure_city: str, arrival_city: str
) -> list:
    """Returns the list of all the known geographical coordinates of
    a specific railway between a given departure city and an arrival city
    From the geographical coordinates of both the cities, from the railways
    identification number linked to the cities in the __init__ file, the algorithm
    looks for geographical points that are located within the two cities.
    Every time a geographical point holds this condition, it is added to the railpath
    list.

    Args:
        railway_id (int): the railway id from which the geo points are given
        departure_city (str): the departure city of the railway link
        arrival_city (str): the arrival city of the railway link

    Returns:
        list: A list of the geographical coordinates of the railway between the
        departure city and the arrival city (until close to more or less 300m)
        The list is a tuple list, stored following the conventional format (lat, long)
    """
    selected_railway_section_geo_list = railway_geo_df[
        railway_geo_df["CODE_LIGNE"] == railway_id
    ]["Geo Shape"]

    selected_railway_section_geo_point = []

    (departure_railstation_geo_point, arrival_railstation_geo_point) = (
        get_coords_for_city_pair(departure_city, arrival_city)
    )

    trip_distance = distance.geodesic(
        departure_railstation_geo_point, arrival_railstation_geo_point
    )

    for selected_railway_section in selected_railway_section_geo_list:
        stop_found = False
        # turn the LineString in dictionnary {"coordinates", "type"} using json module
        selected_railway_section_dict = json.loads(selected_railway_section)

        # extract only coordinates and concatenate them together
        selected_railway_section_to_reverse = selected_railway_section_dict[
            "coordinates"
        ]

        if len(selected_railway_section_to_reverse) == 0:
            continue

        # coordinates in the SNCF file are stored in reverse side,
        # outputed in format long / lat in the csv,
        # instead of the conventional lat / long format
        lat_long_railway_section = [
            (x, y) for y, x in selected_railway_section_to_reverse
        ]

        # compute the geodesic distance between the railpath extrema and
        # the position of departure and arrival
        distance_from_start_to_departure = distance.geodesic(
            lat_long_railway_section[0], departure_railstation_geo_point
        )
        distance_from_start_to_arrival = distance.geodesic(
            lat_long_railway_section[0], arrival_railstation_geo_point
        )

        distance_from_end_to_departure = distance.geodesic(
            lat_long_railway_section[-1], departure_railstation_geo_point
        )
        distance_from_end_to_arrival = distance.geodesic(
            lat_long_railway_section[-1], arrival_railstation_geo_point
        )

        # if both beginning and end of the path exceed the trip distance
        # the path doesn't match at all
        if (
            distance_from_start_to_departure > trip_distance
            and distance_from_end_to_departure > trip_distance
        ) or (
            distance_from_start_to_arrival > trip_distance
            and distance_from_end_to_arrival > trip_distance
        ):
            logger.debug("Some given railways are out of bounds")
            continue

        # otherwise, for each point of the current rail section
        # check if there is a stop point within the rail section
        if (
            distance_from_start_to_departure > trip_distance
            or distance_from_start_to_arrival > trip_distance
        ):
            # look for the beginning of the railpath
            for geo_coord in lat_long_railway_section:
                if (
                    abs(
                        distance.geodesic(geo_coord, departure_railstation_geo_point)
                        - trip_distance
                    )
                    < 0.3
                    or abs(
                        distance.geodesic(geo_coord, arrival_railstation_geo_point)
                        - trip_distance
                    )
                    < 0.3
                ):
                    logger.debug("Arrival railstation found ! Good job !")
                    stop_index = lat_long_railway_section.index(geo_coord)
                    stop_found = True
                    break

            if stop_found:
                lat_long_railway_section = lat_long_railway_section[stop_index:]

        elif (
            distance_from_end_to_departure > trip_distance
            or distance_from_end_to_arrival > trip_distance
        ):
            # look for the end of the railpath
            for geo_coord in list(reversed(lat_long_railway_section)):
                if (
                    abs(
                        distance.geodesic(geo_coord, departure_railstation_geo_point)
                        - trip_distance
                    )
                    < 0.3
                    or abs(
                        distance.geodesic(geo_coord, arrival_railstation_geo_point)
                        - trip_distance
                    )
                    < 0.3
                ):
                    stop_index = lat_long_railway_section.index(geo_coord)
                    stop_found = True
                    break

            # if a stop point has been found, retrieve data until this point
            if stop_found:
                lat_long_railway_section = lat_long_railway_section[:stop_index]

        selected_railway_section_geo_point.append(lat_long_railway_section)

    return selected_railway_section_geo_point
