"""Data loading module"""

import pandas as pd
import streamlit as st
import itertools

CSV_PATH = "./data/raw/regularite-mensuelle-tgv-aqst.csv"


@st.cache_data  # mémorise le résultat d’une fonction pour éviter de la recalculer à
# chaque interaction Streamlit.
# Le décorateur @st.cache_data, qui permet via un cache,
# aux développeurs d'ignorer certains calculs coûteux lorsque
# leurs applications sont réexécutées, joue un rôle important.

def load_data(source: str = CSV_PATH) -> pd.DataFrame:
    """Charge un fichier csv, de séparateurs ";", utilisé pour l'analyse de données

    Args:
        source (str): input de type input = st.sidebar.file_uploader()

    Returns:
        df (pd.DataFrame): retourne le csv converti en DataFrame
    """

    df = pd.read_csv(source, sep=";")
    df = df[["Gare de départ", "Gare d'arrivée", "Retard moyen des trains en retard au départ"]]
    df = df.rename(
        columns={
            "Gare de départ": "GareDepart",
            "Gare d'arrivée": "GareArrivee",
            "Retard moyen des trains en retard au départ": "RetMoyDepart",
        }
    )
    return df


def init() -> None:
    """Initialization function to make global input csv dataframe"""
    global df
    df = load_data()

def get_unique_city_pairs_list() -> list:

    railway_cities = df[["GareDepart","GareArrivee"]]

    unique_railway_cities = railway_cities.value_counts().index.to_list()

    return unique_railway_cities

def get_reachable_destinations_list_from_city(departure: str) -> list:

    reachable_destinations = []

    city_pairs = get_unique_city_pairs_list()

    reachable_destinations = list(itertools.chain(*[city_pair for city_pair in city_pairs if departure in city_pair]))
    # one doesn't need to go directly to the place he came from, unless he needs an alibi...
    reachable_destinations.remove(departure)

    return reachable_destinations


def get_unique_stations_df() -> pd.DataFrame:
    """Gets a dataframe list of all the departure stations of the country

    Returns:
        pd.DataFrame: Departure stations dataframe
    """

    gares = sorted(list(df["GareDepart"].unique()))

    return gares


def file_upload() -> pd.DataFrame:
    """Affiche la barre latérale avec les modules choisis

    Returns:
        pd.Dataframe: le dataframe contenant les données importées
    """

    file_uploader = st.sidebar.file_uploader(
        "Charger un CSV (colonnes: Gares, Retards ...)", type=["csv"]
    )

    # Si l'utilisateur ne charge rien, on utilise le CSV d'exemple fourni
    if file_uploader is not None:
        df = load_data(file_uploader)
    else:
        df = load_data("data/raw/regularite-mensuelle-tgv-aqst.csv")
        st.sidebar.info(
            "Aucun fichier chargé : utilisation de `regularite-mensuelle-tgv-aqst.csv`."
        )

    st.sidebar.write(f"**{len(df)}** données chargées")

    return df


def get_mean_departure_delay_df(departure_city: str) -> pd.DataFrame:
    """Returns the list of the mean delays of a departure city

    Args:
        departure_city (str): Departure city

    Returns:
        pd.DataFrame: Mean delays of a departure city
    """

    return df.loc[df["GareDepart"] == departure_city]["RetMoyDepart"]
