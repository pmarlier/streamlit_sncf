from core import railway_data
from unidecode import unidecode
import pandas as pd
import json
import itertools

CSV_GEO_PATH = "./data/raw/lignes-par-region-administrative.csv"
CSV_RAILSTATIONS_PATH = "./data/raw/liste-des-gares.csv"

def load_railway_geo_data(filepath: str = CSV_GEO_PATH) -> pd.DataFrame:
    """Load geographical points dataframe from all the French railway network

    Args:
        filepath (str, optional): The filepath of the csv file furnished by . Defaults to CSV_PATH.

    Returns:
        pd.DataFrame: _description_
    """
    try:
        railway_geo_df = pd.read_table(filepath, delimiter=";")
    except Exception as exception:
        print(f"{__name__} : FAIL Loading geo file at {filepath}")
        return None

    return railway_geo_df


def load_railstation_geo_data(filepath: str = CSV_RAILSTATIONS_PATH) -> pd.DataFrame:
    """_summary_

    Args:
        filepath (str, optional): _description_. Defaults to CSV_RAILSTATIONS_PATH.

    Returns:
        pd.DataFrame: _description_
    """
    railstation_geo_df = pd.read_table(filepath, delimiter=";")
    railstation_geo_df["LIBELLE"] = [unidecode(railway_station.lower().replace(" ", "-")) for railway_station in railstation_geo_df["LIBELLE"]]
    return railstation_geo_df


def init() -> None:
    """_summary_
    """
    global railway_geo_df
    global railstation_geo_df
    
    railway_geo_df = load_railway_geo_data()
    railstation_geo_df = load_railstation_geo_data()

def build_geo_box_for_city_pair(departure_city:str, arrival_city:str) -> list:
    """_summary_

    Args:
        departure_city (str): _description_
        arrival_city (str): _description_

    Returns:
        list: The geo bounding box encompassing departure and arrival cities
        The bounding box coordinates are stored under the format [min_latitude (N/S), max_latitude (N/S), min_longitude (E/W), max_longitude (E/W)]
    """
    geo_box = [0, 0, 0, 0]
    departure_railstation_geo = railstation_geo_df[railstation_geo_df["LIBELLE"] == railway_data.get_processed_city_name(departure_city)]
    arrival_railstation_geo = railstation_geo_df[railstation_geo_df["LIBELLE"] == railway_data.get_processed_city_name(arrival_city)]

    departure_railstation_geo_point = departure_railstation_geo["Geo Point"].values[0].split(", ")
    arrival_railstation_geo_point = arrival_railstation_geo["Geo Point"].values[0].split(", ")

    try: 
        sorted_latitude = sorted([float(arrival_railstation_geo_point[0]), float(departure_railstation_geo_point[0])])
        sorted_longitude = sorted([float(arrival_railstation_geo_point[1]), float(departure_railstation_geo_point[1])])

        geo_box = list(itertools.chain(*[sorted_latitude, sorted_longitude]))
    except:
        print(f"{__name__} : Fail building geo box for {departure_city} and {arrival_city}, returning {geo_box}")
    
    return geo_box

def is_in_bounding_box(latitude:float, longitude:float, bounding_box:list) -> bool:

    test_1 = bounding_box[0] <= latitude <= bounding_box[1] or bounding_box[2] >= longitude >= bounding_box[3]

    # TODO : fix bounding box algorithm
    # test_2 = bounding_box[0] >= latitude >= bounding_box[1] or bounding_box[2] <= longitude <= bounding_box[3]
    # return test_1 or test_2

    return test_1

def get_railway_geo_point_by_id(railway_id:int, departure_city:str, arrival_city:str) -> list:
    """_summary_

    Args:
        railway_id (int): _description_
        departure_city (str): _description_
        arrival_city (str): _description_

    Returns:
        list: _description_
    """
    selected_railway_section_geo_list = railway_geo_df[railway_geo_df["CODE_LIGNE"] == railway_id]["Geo Shape"]

    selected_railway_section_geo_point = []

    for selected_railway_section in selected_railway_section_geo_list:
        # turn the LineString in dictionnary {"coordinates", "type"}
        selected_railway_section_dict = json.loads(selected_railway_section)
        # extract only coordinates and concatenate them together
        selected_railway_section_to_reverse = selected_railway_section_dict["coordinates"]

        bounding_box = build_geo_box_for_city_pair(departure_city, arrival_city)

        # coordinates stored in reverse side, outputed in format long / lat in the csv, instead of the conventional lat / long format
        lat_long_railway_section = [(x, y) for y, x in selected_railway_section_to_reverse 
                                    if is_in_bounding_box(x,y,bounding_box)]

        if len(lat_long_railway_section) > 0:
            selected_railway_section_geo_point.append(lat_long_railway_section)
    
    # remove duplicated coordinates
    return selected_railway_section_geo_point