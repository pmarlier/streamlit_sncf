import logging.config

import streamlit as st

from core import load_data as ld
from core import railway_data
from core.railway_data import railway_geo
from core.statistics import mean_delay as md

logger: logging.Logger

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


def set_railway_id_network(railway_map: dict) -> None:
    """Setter for the static railway network map
    The network has been built looking iteratively at the known railway id
    moving from both arrival and departure city
    By drawing all the railway section, one could have seen which one was useful
    and which one was not leading to the given city.
    Once removed manually, the network map has been set to static
    """
    global railway_id_network_dict
    railway_id_network_dict = railway_map


def init() -> None:
    """Initialize logger and set the static railway network map"""
    global logger
    logging.config.fileConfig("config/logging.conf")
    logger = logging.getLogger(__name__)
    set_railway_id_network(railway_data.RAILWAY_ID_NETWORK)


def get_railway_id_from_network(departure: str, arrival: str) -> list:
    """From city pair from the original SNCF delay dataframe, the main one to
    work on during this project, retrieve the railway ids after processing railstation
    names to keep consistency between SNCF datasets (it was not originally the case)

    Args:
        departure_city (str): the departure city of the railway link
        arrival_city (str): the arrival city of the railway link

    Returns:
        list: the list of railways id linking the departure and the arrival cities
    """
    try:
        railway_id = railway_id_network_dict[
            f"{railway_data.get_processed_city_name(departure)}-{railway_data.get_processed_city_name(arrival)}"
        ]
    except Exception:
        logger.debug(
            f"Unable to find {departure}-{arrival} (no geo data in foreign country)"
        )
        return []

    logger.debug(f"Railways retrieved for {departure}-{arrival}")
    return railway_id


@st.cache_data
def get_railway_data_between_cities(departure: str, arrival: str) -> list:
    """Build the custom list of data about railway geo points and delay from city pair
    to be displayed on the Folium map. The mean delay gives the color of the displayed
    line. Delay and both cities are displayed on hover.
    Of course, the railway geographical data points are used to effectively draw the
    polylines.

    Args:
        departure_city (str): the departure city of the railway link
        arrival_city (str): the arrival city of the railway link

    Returns:
        list: the list of required data to draw railways information on the FOLIUM map
            list[0] : railway_id : used only to check consistency
            list[1] : railway_point_to_draw : the geographical railway data points
            list[2] : departure : the departure city of the railway link (hover)
            list[3] : arrival_city : the arrival city of the railway link (hover)
            list[4] : mean_delay : match the colormap of national delay statistics
    """
    md.init()
    # retrieve delay data to be displayed on the map
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

    logger.debug(f"Data retrieved {departure}-{arrival}")
    return railway_data_to_draw


@st.cache_data
def get_all_railways_to_draw() -> list:
    """Build the custom list of data about railway geo points and delay for all
    the railstation pairs listed in the original SNCF dataset

    Returns:
        list: a list of the list of required data to draw railways information
        on the FOLIUM map for each city pair of the original dataframe.
        For each railway link, one can find all the following output data:
            list[0] : railway_id : used only to check consistency
            list[1] : railway_point_to_draw : the geographical railway data points
            list[2] : departure : the departure city of the railway link (hover)
            list[3] : arrival_city : the arrival city of the railway link (hover)
            list[4] : mean_delay : match the colormap of national delay statistics
    """

    all_railways_data_to_draw = []
    city_pairs = ld.get_unique_city_pairs_list()

    for city_pair in city_pairs:
        departure, arrival = city_pair
        all_railways_data_to_draw.append(
            get_railway_data_between_cities(departure, arrival)
        )

    return all_railways_data_to_draw
