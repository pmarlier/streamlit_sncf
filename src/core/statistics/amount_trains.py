"""This module computes from given departure and arrival stations, the ratio of delayed
at departure and arrival, and cancelled trains. The ratio is computed
from the amount of delayed/cancelled trains over the total planned trains on a given
period."""

import pandas as pd
import numpy as np
from core import load_data as ld
from core.statistics.mean_delay import ratio_number_of_trains


def get_ratio_cancelled_trains(
    departure_station: str,
    arrival_station: str,
    start_month: int,
    end_month: int,
    years_list: np.array,
    data_df: pd.DataFrame | None = None,
) -> float:
    """Calculate the ratio of cancelled trains 
    to the total number of planned trains
    over a period, given a departure and arrival stations.

    The ratio is calculated using only valid monthly observations.

    Args:
        departure_station (str): departure station
        arrival_station (str): arrival station
        start_month (int): start month of period
        end_month (int): end month of period
        years_list (np.array): selected years list
        data_df (pd.DataFrame): input dataframe with MONTH, YEAR, DEPARTURE_STATION_KEY
        and ARRIVAL_STATION_KEY columns

    Returns:
        cancelled_trains_ratio (float): the ratio of cancelled trains
            to the total number of planned trains
            over a period between two given stations,
            or NaN if no valid observations are available
    """
    if data_df is None:
        data_df = ld.df

    df_stations = ld.get_filtered_departure_arrival_stations_df(
        departure_station, arrival_station, data_df
    )
    df_period = ld.get_filtered_period_df(
        start_month, end_month, years_list, df_stations
    )
    # calculate the ratio for the valid monthly observations
    cancelled_trains_ratio = ratio_number_of_trains(
        df_period[ld.MONTHLY_PLANNED_TRAINS_KEY],
        df_period[ld.MONTHLY_CANCELLED_TRAINS_KEY],
    )
    return cancelled_trains_ratio


def get_total_planned_trains(departure_station: str, 
                               arrival_station: str,  
                               start_month: int, end_month: int,
                               years_list: np.array,
                               data_df: pd.DataFrame | None = None) -> int:
    """Returns the amount of planned trains over a period, 
    given a departure and arrival stations

    Args:
        departure_station (str): departure station
        arrival_station (str): arrival station
        start_month (int): start month of period
        end_month (int): end month of period
        years_list (np.array): selected years list
        data_df (np.array): input dataframe with MONTH, YEAR, DEPARTURE_STATION_KEY 
        and ARRIVAL_STATION_KEY columns

    Returns:
        planned_trains_amount (int): the amount of planned trains
        over a period between two given stations
    """
    if data_df is None:
        data_df = ld.df
            
    df_stations = ld.get_filtered_departure_arrival_stations_df(departure_station, arrival_station, data_df)
    df_period = ld.get_filtered_period_df(start_month, end_month, years_list, df_stations)
    if df_period[ld.MONTHLY_PLANNED_TRAINS_KEY].empty:
        planned_trains_amount = np.nan
    else:
        planned_trains_amount = df_period[ld.MONTHLY_PLANNED_TRAINS_KEY].sum()
    # planned_trains_amount = df_period[ld.MONTHLY_PLANNED_TRAINS_KEY].sum(min_count=1)

    return planned_trains_amount


def get_ratio_delayed_departure_trains(
    departure_station: str,
    arrival_station: str,
    start_month: int,
    end_month: int,
    years_list: np.array,
    data_df: pd.DataFrame | None = None,
) -> float:
    """Calculate the ratio of delayed trains at departure 
    to the total number of planned trains,
    over a selected period and
    given a departure and arrival stations.

    The ratio is calculated using only valid monthly observations.

    Args:
        departure_station (str): departure station
        arrival_station (str): arrival station
        start_month (int): start month of period
        end_month (int): end month of period
        years_list (np.array): selected years list
        data_df (pd.DataFrame): input dataframe with MONTH, YEAR, DEPARTURE_STATION_KEY
        and ARRIVAL_STATION_KEY columns

    Returns:
        delayed_departure_trains_ratio (float): the ratio of delayed trains
        at departure to the total number of planned trains
        over a period between two given stations,
        or NaN if no valid observations are available.
    """
    if data_df is None:
        data_df = ld.df

    df_stations = ld.get_filtered_departure_arrival_stations_df(
        departure_station, arrival_station, data_df
    )
    df_period = ld.get_filtered_period_df(
        start_month, end_month, years_list, df_stations
    )
    # calculate the ratio for the valid monthly observations
    delayed_departure_trains_ratio = ratio_number_of_trains(
        df_period[ld.MONTHLY_PLANNED_TRAINS_KEY],
        df_period[ld.MONTHLY_DELAYED_DEPARTURE_TRAINS_KEY],
    )
    # delayed_departure_trains_amount = df_period[ld.MONTHLY_DELAYED_DEPARTURE_TRAINS_KEY].sum(min_count=1)

    return delayed_departure_trains_ratio


def get_ratio_delayed_arrival_trains(
    departure_station: str,
    arrival_station: str,
    start_month: int,
    end_month: int,
    years_list: np.array,
    data_df: pd.DataFrame | None = None,
) -> float:
    """Calculate the ratio of delayed trains at arrival 
    to the total number of planned trains,
    over a selected period and
    given a departure and arrival stations.

    The ratio is calculated using only valid monthly observations.

    Args:
        departure_station (str): departure station
        arrival_station (str): arrival station
        start_month (int): start month of period
        end_month (int): end month of period
        years_list (np.array): selected years list
        data_df (pd.DataFrame): input dataframe with MONTH, YEAR, DEPARTURE_STATION_KEY
        and ARRIVAL_STATION_KEY columns

    Returns:
        delayed_arrival_trains_ratio (float): the ratio of delayed trains 
        at arrival to the total number of planned trains
        over a period between two given stations,
        or NaN if no valid observations are available.
    """
    if data_df is None:
        data_df = ld.df

    df_stations = ld.get_filtered_departure_arrival_stations_df(
        departure_station, arrival_station, data_df
    )
    df_period = ld.get_filtered_period_df(
        start_month, end_month, years_list, df_stations
    )
    # calculate the ratio for the valid monthly observations
    delayed_arrival_trains_ratio = ratio_number_of_trains(
        df_period[ld.MONTHLY_PLANNED_TRAINS_KEY],
        df_period[ld.MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY],
    )
    # delayed_arrival_trains_amount = df_period[ld.MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY].sum(min_count=1)

    return delayed_arrival_trains_ratio
