"""Mean delay computing module feeding UI functions"""

import numpy as np
import pandas as pd
from core import load_data as ld


# def liste_retards_moyens_france(df: pd.DataFrame) -> pd.DataFrame:
#     """Filtre la liste complète selon les retards moyens
#     au départ de toutes les gares de France

#     Args:
#         df (pd.DataFrame): DataFrame complet

#     Returns:
#         df2 (pd.DataFrame): le dataframe filtré"""

#     gares = sorted(list(df["GareDepart"].unique()))
#     RetMoy = [df.loc[df["GareDepart"] == gare]["RetMoyDepart"].mean() for gare in gares]
#     df2 = pd.DataFrame(np.array([gares, RetMoy]).T, columns=["GareDepart", "RetMoy"])

#     return df2

def get_departure_mean_delay_for_city(city: str) -> float:
    return ld.df.loc[ld.df[ld.GARE_DEPART_KEY] == city][ld.RETARD_MOYEN_DEPART_KEY].mean()

def get_arrival_mean_delay_for_city_pair(departure: str, arrival: str) -> float:
    departure_df = ld.df[ld.df[ld.GARE_DEPART_KEY] == departure]
    departure_arrival_df = departure_df[departure_df[ld.GARE_ARRIVEE_KEY] == arrival]
    return departure_arrival_df[ld.RETARD_MOYEN_DEPART_KEY].mean()

def get_departure_city_mean_delay_df(
    df: pd.DataFrame, departure_city: str
) -> pd.DataFrame:
    """Returns a dataframe containing the mean delay from a departure city, to display the horizontal reference on histogram

    Args:
        df (pd.DataFrame): Dataframe from which get the length
        departure_city (str): Departure city to compute the mean departure delays from

    Returns:
        pd.DataFrame: Dataframe duplicating the computed mean departure delays
        of the length of df
    """
    
    return pd.DataFrame(
        data=np.ones(np.shape(df)[0])
        * ld.df.loc[ld.df[ld.GARE_DEPART_KEY] == departure_city][ld.RETARD_MOYEN_DEPART_KEY].mean()
    )


def get_national_global_delay_mean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a dataframe containing the mean delay of the whole country, to display the horizontal reference on histogram

    Args:
        df (pd.DataFrame): Dataframe from which get the length

    Returns:
        pd.DataFrame: Dataframe duplicating the computed mean departure delays
        of the length of df
    """
    return pd.DataFrame(data=np.ones(np.shape(df)[0]) * ld.df[ld.RETARD_MOYEN_DEPART_KEY].mean())
