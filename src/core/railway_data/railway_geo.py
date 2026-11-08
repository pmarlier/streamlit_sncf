import json

import pandas as pd
from geopy import distance
from unidecode import unidecode

from core import railway_data

CSV_GEO_PATH = "./data/raw/lignes-par-region-administrative.csv"
CSV_RAILSTATIONS_PATH = "./data/raw/liste-des-gares.csv"


def load_railway_geo_data(filepath: str = CSV_GEO_PATH) -> pd.DataFrame:
    """Load geographical points dataframe from all the French railway network

    Args:
        filepath (str, optional): The filepath of the csv file furnished by .
        Defaults to CSV_PATH.

    Returns:
        pd.DataFrame: _description_
    """
    try:
        railway_geo_df = pd.read_table(filepath, delimiter=";")
    except Exception:
        print(f"{__name__} : FAIL Loading railway geo file at {filepath}")
        return None

    return railway_geo_df


def load_railstation_geo_data(filepath: str = CSV_RAILSTATIONS_PATH) -> pd.DataFrame:
    """_summary_

    Args:
        filepath (str, optional): _description_. Defaults to CSV_RAILSTATIONS_PATH.

    Returns:
        pd.DataFrame: _description_
    """
    try:
        railstation_geo_df = pd.read_table(filepath, delimiter=";")
        railstation_geo_df["LIBELLE"] = [
            unidecode(railway_station.lower().replace(" ", "-"))
            for railway_station in railstation_geo_df["LIBELLE"]
        ]
    except Exception:
        print(f"{__name__} : FAIL Loading railstation geo file at {filepath}")
        return None

    return railstation_geo_df


def set_railway_geo_df(dataframe: pd.DataFrame) -> None:
    global railway_geo_df
    railway_geo_df = dataframe


def set_railstation_geo_df(dataframe: pd.DataFrame) -> None:
    global railstation_geo_df
    railstation_geo_df = dataframe


def init() -> None:
    """_summary_"""
    set_railway_geo_df(load_railway_geo_data())
    set_railstation_geo_df(load_railstation_geo_data())


def get_coords_for_city_pair(departure_city: str, arrival_city: str) -> list:
    """_summary_

    Args:
        departure_city (str): _description_
        arrival_city (str): _description_

    Returns:
        list: The geo bounding box encompassing departure and arrival cities
        The bounding box coordinates are stored under the format [min_latitude (N/S),
        max_latitude (N/S), min_longitude (E/W), max_longitude (E/W)]
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

    return departure_railstation_geo_point, arrival_railstation_geo_point


def get_railway_geo_point_by_id(
    railway_id: int, departure_city: str, arrival_city: str
) -> list:
    """_summary_

    Args:
        railway_id (int): _description_
        departure_city (str): _description_
        arrival_city (str): _description_

    Returns:
        list: _description_
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
            continue

        # check if the current rail section exceeds the path
        # between departure and arrival
        if (
            distance_from_start_to_departure > trip_distance
            or distance_from_start_to_arrival > trip_distance
        ):
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
                    stop_index = lat_long_railway_section.index(geo_coord)
                    stop_found = True
                    break

            if stop_found:
                lat_long_railway_section = lat_long_railway_section[stop_index:]

        elif (
            distance_from_end_to_departure > trip_distance
            or distance_from_end_to_arrival > trip_distance
        ):
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

            if stop_found:
                lat_long_railway_section = lat_long_railway_section[:stop_index]

        selected_railway_section_geo_point.append(lat_long_railway_section)

    # remove duplicated coordinates
    return selected_railway_section_geo_point
