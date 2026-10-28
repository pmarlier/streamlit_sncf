import numpy as np

import pandas as pd

from core import load_data as ld


def calculate_mean_arrival_delay_distribution_per_month(
    departure_station: str, 
    arrival_station: str,  
    selected_month: int, 
    historical_years: list[int],
    data_df: pd.DataFrame,
) -> dict[str, float | int | None]:
    """Return different statistics about the mean train delays at arrival
    for a specific calendar month of the year and a specific railway line.

    The distribution is calculated using the monthly mean of arrival delays
    from the selected historical years.

    Statistics are calculated depending on the number of available
    and valid observations:
        - 0 observation: all statistics are NaN
        - 1 observation: median only
        - 2 to 4 observations: minimum, median and maximum
        - 5+ observations: minimum, Q1, median, Q3 and maximum
    It adds also to these statistics the sum of delayed trains at arrival
    used for the calculation of the mean if values are valid and available,
    and the number of observations (number of years).

    Unavailable statistics are represented by NaN.
    The sum of delayed trains at arrival is None when it cannot be determined.

    Args:
        departure_station (str): departure railway station
        arrival_station (str): arrival railway station
        selected_month (int): calendar month (1 to 12)
        historical_years (list[int]): selected years which should be 
            available in the dataset
        data_df (pd.DataFrame): dataFrame containing the preprocessed data

    Returns:
        dict[str, float | int | None]: 
            - minimum: minimum of monthly mean delay (minutes)
            - q1: first quartile of monthly mean delay (minutes)
            - median: median of monthly mean delay (minutes)
            - q3: third quartile of monthly mean delay (minutes)
            - maximum: maximum of monthly mean delay (minutes)
            - number_historical_year_observations: number of valid observations
            - sum_arr_delayed_trains: sum of delayed trains used to calculate
                the monthly mean arrival delays. Only the observations with valid 
                monthly means are included in this sum.
    """
    
    # TODO: Handle multiple observations for the same train line, year and month.
    # This should be done in data_preprocessing.py.

    df_stations = ld.get_filtered_departure_arrival_stations_df(
        departure_station, 
        arrival_station, 
        data_df
    )

    df_period = ld.get_filtered_period_df(
        selected_month, 
        selected_month, 
        historical_years, 
        df_stations
    )

    # delete the lines with NaN in the mean of arrival delay column
    df_cleaned = df_period.dropna(subset=[ld.MEAN_ARRIVAL_DELAY_KEY])

    # get the monthly delay means
    historical_delays = df_cleaned[ld.MEAN_ARRIVAL_DELAY_KEY]

    # get the numbers of delayed trains used for the mean of delay calculation
    arr_delayed_trains = df_cleaned[ld.MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY]

    # return the sum of delayed trains if there is no NaN 
    # in the observations of delayed trains
    # return None if there is at leat one NaN or no obervations at all
    if arr_delayed_trains.notna().all() and not arr_delayed_trains.empty:
        sum_arr_delayed_trains = int(arr_delayed_trains.sum())
    else:
        sum_arr_delayed_trains = None

    # calculate the number of observations
    number_observations = len(historical_delays)

    # Initialize the dictionnary of statistics
    arr_delays_per_month_statistics = {
        "minimum": np.nan,
        "q1": np.nan,
        "median": np.nan,
        "q3": np.nan,
        "maximum": np.nan,
        "number_historical_year_observations": number_observations,
        "sum_arr_delayed_trains": sum_arr_delayed_trains,
    }

    # calculate (and sometimes return) the statistics of the distribution
    # depending on the number of observations available
    if number_observations == 0:
        return arr_delays_per_month_statistics
    elif number_observations == 1:
        arr_delays_per_month_statistics["median"] = historical_delays.median()
    elif number_observations >=2 and number_observations <=4:
        arr_delays_per_month_statistics["minimum"] = historical_delays.min()
        arr_delays_per_month_statistics["median"] = historical_delays.median()
        arr_delays_per_month_statistics["maximum"] = historical_delays.max()
    else:
        arr_delays_per_month_statistics["minimum"] = historical_delays.min()
        arr_delays_per_month_statistics["q1"] = historical_delays.quantile(0.25)
        arr_delays_per_month_statistics["median"] = historical_delays.median()
        arr_delays_per_month_statistics["q3"] = historical_delays.quantile(0.75)
        arr_delays_per_month_statistics["maximum"] = historical_delays.max()

    # return the statistics
    return arr_delays_per_month_statistics
