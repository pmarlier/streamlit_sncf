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

def weighted_mean_delay(
    monthly_planned_trains: pd.Series, 
    delay_observations_to_average: pd.Series
) -> float:
    """Calculate a weighted mean of a series of delay observations weighted by 
    the number of trains planned for each period. 
    
    This function can be used to calculate weighted means of the departure or 
    arrival delays. 

    Both input Series must cover the same periods and have matching indexes.
    Observations with missing values or non-positive (<= 0) 
    monthly planned train counts are excluded.
    
    Args:
        monthly_planned_trains (pd.Series): the number of planned trains 
            on the selected months.
            This Series should normally come from the MONTHLY_PLANNED_TRAINS_KEY. 
            The Pandas Series must be filtered to only include the periods you want 
            to include in the calculation.

        delay_observations_to_average (pd.Series): the delay measure or 
            observations you wish to get the mean. 
            The Pandas Series must be filtered to only include the 
            periods you want to average.

    Returns:
        float: the delay weighted mean of the valid observations,
            or NaN if no valid observations are available.
    """

    # Creating a mask to select non-NaN values and 
    # strictly positive monthly_planned_trains values
    valid_values = (
        monthly_planned_trains.notna() 
        & (monthly_planned_trains > 0) 
        & delay_observations_to_average.notna()
    )

    # Returning a NaN if no valid observation could be used 
    if not valid_values.any():
        return np.nan

    weighted_mean = float(
        np.average(
            delay_observations_to_average[valid_values], 
            weights=monthly_planned_trains[valid_values],
        )
    )

    return weighted_mean


def ratio_number_of_trains(
    monthly_planned_trains: pd.Series, 
    train_observations: pd.Series
) -> float:
    """Calculate the ratio of observed trains to planned trains.

    This function can be used to calculate the proportion of delayed or
    cancelled trains among planned trains over the selected periods.

    Both input Series must cover the same periods and have matching indexes.
    Observations with missing values or invalid counts are excluded.

    Args:
        monthly_planned_trains (pd.Series): Number of planned trains for each
            selected month, usually from MONTHLY_PLANNED_TRAINS_KEY.
            The Series must be filtered to the periods being studied.

        train_observations (pd.Series): Number of delayed or cancelled trains
            for each selected month. The Series must cover the same periods
            as monthly_planned_trains.

    Returns:
        float: The ratio of valid train observations to planned trains,
            or NaN if no valid observations are available.
    """

    # Creating a mask to select non-NaN values, positive planned counts 
    # and non-negative observations
    valid_values = (
        monthly_planned_trains.notna()
        & (monthly_planned_trains > 0)
        & train_observations.notna()
        & (train_observations >= 0)
    )

    # Returning NaN if no valid observations could be used
    if not valid_values.any():
        return np.nan

    train_ratio = float(
        train_observations[valid_values].sum()
        / monthly_planned_trains[valid_values].sum()
    )

    return train_ratio
    

def get_departure_mean_delay_for_city(city: str) -> float:
    return ld.df.loc[ld.df[ld.DEPARTURE_STATION_KEY] == city][ld.MEAN_DEPARTURE_DELAY_KEY].mean()

def get_arrival_mean_delay_for_city_pair(departure: str, arrival: str) -> float:
    departure_df = ld.df[ld.df[ld.DEPARTURE_STATION_KEY] == departure]
    departure_arrival_df = departure_df[departure_df[ld.ARRIVAL_STATION_KEY] == arrival]
    return departure_arrival_df[ld.MEAN_DEPARTURE_DELAY_KEY].mean()

def get_departure_city_mean_delay_df(
    df: pd.DataFrame, departure_city: str
) -> pd.DataFrame:
    """Returns a dataframe containing the mean delay from a departure city, to display
    the horizontal reference on histogram

    Args:
        df (pd.DataFrame): Dataframe from which get the length
        departure_city (str): Departure city to compute the mean departure delays from

    Returns:
        pd.DataFrame: Dataframe duplicating the computed mean departure delays
        of the length of df
    """
    
    return pd.DataFrame(
        data=np.ones(np.shape(df)[0]) * ld.df.loc[ld.df[ld.DEPARTURE_STATION_KEY] 
                                                  == departure_city][ld.MEAN_DEPARTURE_DELAY_KEY].mean()
    )


def get_national_global_delay_mean_df(df: pd.DataFrame) -> pd.DataFrame:
    """Returns a dataframe containing the mean delay of the whole country, to display the horizontal reference on histogram

    Args:
        df (pd.DataFrame): Dataframe from which get the length

    Returns:
        pd.DataFrame: Dataframe duplicating the computed mean departure delays
        of the length of df
    """
    return pd.DataFrame(data=np.ones(np.shape(df)[0]) * ld.df[ld.MEAN_DEPARTURE_DELAY_KEY].mean())