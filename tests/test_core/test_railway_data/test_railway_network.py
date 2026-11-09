import pytest
import pandas as pd
from core.railway_data import railway_network
import core.railway_data as railway_data
import core.load_data as ld

MOCKED_RAILWAY_ID_NETWORK = {  # OK
    "paris-montparnasse-pasteur-rennes": [101],
}


def test_get_processed_city_name():
    """To match city names from different files produced by SNCF:
        we had to build mapping and preprocessing before feeding the pipeline

        As a reminder, here is the MAP used in the source code

        MAP_CITY = {
        "lille": "lille-champ-de-mars",
        "paris-lyon": "paris-gare-de-lyon",
        "saint-etienne-chateaucreux": "st-etienne-chateaucreux",
        "angers-saint-laud": "angers-st-laud",
        "macon-loche": "macon-ville",
        "metz": "metz-ville",
        "nancy": "nancy-ville",
        "strasbourg": "strasbourg-ville",
        "valence-alixan-tgv": "valence-tgv",
        "montpellier": "montpellier-sud-de-france",
        "marne-la-vallee": "paris-gare-de-lyon",
        "paris-montparnasse": "paris-montparnasse-pasteur",
        "bellegarde-(ain)": "bellegarde",
        "lyon-part-dieu": "lyon-perrache",

        # as long as we don't have any railway geo coordinates for foreign countries
        # we mapped foreign railstation with the closest city in France
        # that is only for railpath drawing
        "madrid": "perpignan",
        "barcelona": "perpignan",
        "italie": "monaco",
        "francfort": "strasbourg",
        "stuttgart": "strasbourg",
        "zurich": "annecy",
        "lausanne": "annecy",
        "geneve": "annecy",
    }

    """
    # some cities have very different names (from the above mapping)
    assert railway_data.get_processed_city_name("Paris Lyon") == "paris-gare-de-lyon"

    # some cities only need to bo lowered case
    assert railway_data.get_processed_city_name("Rennes") == "rennes"

    # some cities could be already set
    assert railway_data.get_processed_city_name("paris-nord") == "paris-nord"


def test_get_railway_id_from_network():
    """
    Test retrieval of railway IDs from the network dictionary.
    """
    # load the real railway map, and check request result failed
    # as we compare real data with mock expected answer
    railway_network.init()

    # check failed match between mock dictionnary on top of the file
    res_valid = railway_network.get_railway_id_from_network(
        "Paris Montparnasse", "Rennes"
    )
    assert res_valid != [101]

    # and check a real value between Paris and Bordeaux
    res_invalid = railway_network.get_railway_id_from_network(
        "Paris Montparnasse", "Bordeaux St Jean"
    )
    assert res_invalid == [570000]

    # replace the real railway map with the mock one
    railway_network.set_railway_id_network(MOCKED_RAILWAY_ID_NETWORK)

    # this time, check match with mock dictionnary on top of the file
    res_valid = railway_network.get_railway_id_from_network(
        "Paris Montparnasse", "Rennes"
    )
    assert res_valid == [101]

    # and this is an invalid pair as long it is not in the mock dictionnary
    res_invalid = railway_network.get_railway_id_from_network(
        "Paris Montparnasse", "Bordeaux St Jean"
    )
    assert res_invalid == []


def test_get_railway_data_between_cities(mocked_df):
    """
    Test getting full drawing data for a specific city pair.
    """
    departure = "Paris Montparnasse"
    arrival = "Rennes"

    ld.set_monthly_punctuality_rate_df(mocked_df)
    railway_network.set_railway_id_network(MOCKED_RAILWAY_ID_NETWORK)
    result = railway_network.get_railway_data_between_cities(departure, arrival)

    assert len(result) == 1
    # Format: [railway_id, railway_point, departure, arrival, mean_delay]
    assert result[0][0] == 101
    assert result[0][2] == departure
    assert result[0][3] == arrival
    # Since we use mocked_df, we just verify it's a number (even if NaN, it's a float)
    assert isinstance(result[0][4], float)


def test_get_all_railways_to_draw(mocked_df):
    """
    Test gathering all railway data for all unique city pairs.
    """
    ld.set_monthly_punctuality_rate_df(mocked_df)
    result = railway_network.get_all_railways_to_draw()

    assert isinstance(result, list)
    assert len(result) > 0
