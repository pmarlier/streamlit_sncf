import streamlit as st

from core import load_data as ld
from core import railway_data
from core.railway_data import railway_geo
from core.statistics import mean_delay as md

# fusion : "marne-la-vallee - paris-gare-de-lyon"
# pour cause d'absence d'affichage de la ligne

# station name are not written identically between SNCF datasets :
# a bit of processing to make syntax match
# use of UNIDECODE to replace accent and every special character
# with the closest character in ascii
# lower case, replace " " with "-"

# cas particuliers :
# marseille - lyon -> marseille - l'estaque - lyon
# paris - chambery -> chambery - bellegarde - lyon - paris

# anomalies :
# MACON LOCHE - PARIS LYON dans fichier retard,
# mais ligne entre MACON VILLE - PARIS LYON
# PARIS LYON - MULHOUSE dans fichier retard, mais ligne entre PARIS EST - MULHOUSE VILLE


def get_railway_id_from_network(departure: str, arrival: str) -> list:
    """_summary_

    Args:
        departure (str): _description_
        arrival (str): _description_

    Returns:
        list: _description_
    """
    try:
        railway_id = railway_data.RAILWAY_ID_NETWORK[
            f"{railway_data.get_processed_city_name(departure)}-{railway_data.get_processed_city_name(arrival)}"
        ]
    except Exception:
        print(f"{__name__} : FAIL to retrieve a railway for - {departure}-{arrival}")
        return []

    return railway_id


def get_railway_data_from_city(departure: str) -> list:
    """_summary_

    Args:
        departure (str): _description_

    Returns:
        list: _description_
    """
    railway_data_to_draw = []

    reachable_destinations_list = ld.get_reachable_destinations_list_from_city(
        departure
    )

    arrival = reachable_destinations_list[0]

    print(f"{departure} - {arrival}")
    mean_delay_on_arrival = md.get_arrival_mean_delay_for_city_pair(departure, arrival)

    railway_id_list = get_railway_id_from_network(departure, arrival)

    for railway_id_to_draw in railway_id_list:
        railway_point_to_draw = railway_geo.get_railway_geo_point_by_id(
            railway_id_to_draw, departure, arrival
        )
        railway_data_to_draw.append(
            [
                railway_id_to_draw,
                railway_point_to_draw,
                departure,
                arrival,
                mean_delay_on_arrival,
            ]
        )

    return railway_data_to_draw


@st.cache_data
def get_railway_data_between_cities(departure: str, arrival: str) -> list:
    """_summary_

    Args:
        departure (str): _description_
        arrival (str): _description_

    Returns:
        list: _description_
    """
    mean_delay_on_arrival = md.get_arrival_mean_delay_for_city_pair(departure, arrival)
    railway_data_to_draw = []

    railway_id_list = get_railway_id_from_network(departure, arrival)

    for railway_id_to_draw in railway_id_list:
        railway_point_to_draw = railway_geo.get_railway_geo_point_by_id(
            railway_id_to_draw, departure, arrival
        )
        railway_data_to_draw.append(
            [
                railway_id_to_draw,
                railway_point_to_draw,
                departure,
                arrival,
                mean_delay_on_arrival,
            ]
        )

    return railway_data_to_draw


def get_all_railways_to_draw() -> list:
    """_summary_

    Args:
        departure (str): _description_

    Returns:
        list: _description_
    """

    all_railways_data_to_draw = []
    city_pairs = ld.get_unique_city_pairs_list()

    for city_pair in city_pairs:
        departure, arrival = city_pair
        all_railways_data_to_draw.append(
            get_railway_data_between_cities(departure, arrival)
        )

    return all_railways_data_to_draw
