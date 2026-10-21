"""This module computes from given departure and arrival stations, the amount of delayed
at departure and arrival, and cancelled trains. Over each month, the ratio is computed 
from the amount of delayed/cancelled trains over the total planned trains on a given 
period."""

import pandas as pd
import numpy as np
from core import load_data as ld

def get_total_cancelled_trains(departure_station: str, 
                               arrival_station: str,  
                               start_month: int, end_month: int,
                               years_list: np.array,
                               data_df: pd.DataFrame | None = None) -> int:
    """Returns the amount of cancelled trains over a period, 
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
        cancelled_trains_amount (int): return the amount of cancelled trains 
        over a period between two given stations
    """
    if data_df is None:
        data_df = ld.df
            
    df_stations = ld.get_filtered_departure_arrival_stations_df(departure_station, arrival_station, data_df)
    df_period = ld.get_filtered_period_df(start_month, end_month, years_list, df_stations)
    cancelled_trains_amount = sum(df_period[ld.MENSUAL_CANCELLED_TRAINS_KEY])
    
    return cancelled_trains_amount

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
        planned_trains_amount (int): return the amount of planned trains 
        over a period between two given stations
    """
    if data_df is None:
        data_df = ld.df
            
    df_stations = ld.get_filtered_departure_arrival_stations_df(departure_station, arrival_station, data_df)
    df_period = ld.get_filtered_period_df(start_month, end_month, years_list, df_stations)
    planned_trains_amount = sum(df_period[ld.MENSUAL_PLANNED_TRAINS_KEY])

    return planned_trains_amount

def get_total_delayed_departure_trains(departure_station: str, 
                               arrival_station: str,  
                               start_month: int, end_month: int,
                               years_list: np.array,
                               data_df: pd.DataFrame | None = None) -> int:
    """Returns the amount of delayed trains at departure over a period, 
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
        delayed_departure_trains_amount (int): return the amount of delayed trains 
        at departure over a period between two given stations
    """
    if data_df is None:
            data_df = ld.df
            
    df_stations = ld.get_filtered_departure_arrival_stations_df(departure_station, arrival_station, data_df)
    df_period = ld.get_filtered_period_df(start_month, end_month, years_list, df_stations)
    delayed_departure_trains_amount = sum(df_period[ld.MENSUAL_DELAYED_DEPARTURE_TRAINS_KEY])

    return delayed_departure_trains_amount

def get_total_delayed_arrival_trains(departure_station: str, 
                               arrival_station: str,  
                               start_month: int, end_month: int,
                               years_list: np.array,
                               data_df: pd.DataFrame | None = None) -> int:
    """Returns the amount of delayed trains at arrival over a period, 
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
        delayed_arrival_trains_amount (int): return the amount of delayed trains 
        at arrival over a period between two given stations
    """
    if data_df is None:
            data_df = ld.df
            
    df_stations = ld.get_filtered_departure_arrival_stations_df(departure_station, arrival_station, data_df)
    df_period = ld.get_filtered_period_df(start_month, end_month, years_list, df_stations)
    delayed_arrival_trains_amount = sum(df_period[ld.MENSUAL_DELAYED_ARRIVAL_TRAINS_KEY])

    return delayed_arrival_trains_amount