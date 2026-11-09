"""Mean delay computing module feeding UI functions"""

import numpy as np
import pandas as pd

from core import load_data as ld


def weighted_mean_delay(
    monthly_planned_trains: pd.Series, delay_observations_to_average: pd.Series
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


def get_arrival_mean_delay_for_city_pair(departure: str, arrival: str) -> float:
    departure_df = ld.df[ld.df[ld.DEPARTURE_STATION_KEY] == departure]
    departure_arrival_df = departure_df[departure_df[ld.ARRIVAL_STATION_KEY] == arrival]
    return departure_arrival_df[ld.MEAN_DEPARTURE_DELAY_KEY].mean()
