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
        - 0 observations: all distribution statistics are NaN
        - 1 observation: median only
        - 2 to 4 observations: minimum, median and maximum
        - 5+ observations: minimum, Q1, median, Q3 and maximum
    The function also returns the total number of delayed trains at arrival,
    which have been used for the calculation of the means. This number is
    returned only if values are valid and available.
    The function returns also the number of observations
    (number of historical years)

    Unavailable statistics are represented by NaN.
    The total number of delayed trains at arrival is None when
    it cannot be determined.

    Args:
        departure_station (str): departure railway station
        arrival_station (str): arrival railway station
        selected_month (int): calendar month (1 to 12)
        historical_years (list[int]): past years selected for calculations,
            which should be available in the dataset
        data_df (pd.DataFrame): DataFrame containing the preprocessed data

    Returns:
        dict[str, float | int | None]:
            - minimum: minimum of monthly mean delay (minutes)
            - q1: first quartile of monthly mean delay (minutes)
            - median: median of monthly mean delay (minutes)
            - q3: third quartile of monthly mean delay (minutes)
            - maximum: maximum of monthly mean delay (minutes)
            - number_historical_year_observations: number of
                valid observations (historical years)
            - sum_arr_delayed_trains: total number of delayed trains
                    associated with the valid monthly mean arrival delays
    """

    # TODO: Handle multiple observations for the same train line, year and month.
    # This should be done in data_preprocessing.py.

    df_stations = ld.get_filtered_departure_arrival_stations_df(
        departure_station, arrival_station, data_df
    )

    df_period = ld.get_filtered_period_df(
        selected_month, selected_month, historical_years, df_stations
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
    elif number_observations >= 2 and number_observations <= 4:
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


def generate_historical_monthly_mean_arrival_delay_distribution_dataframe(
    departure_station: str,
    arrival_station: str,
    start_month: int,
    end_month: int,
    historical_years: list[int],
    data_df: pd.DataFrame,
) -> pd.DataFrame:
    """Generate a dataframe containing statistics of the mean train delays at arrival
        for each calendar month of the selected period and selected railway line.

        Statistics are calculated from the monthly mean arrival delays observed
        during the selected historical years.

    Args:
        departure_station (str): departure railway station
        arrival_station (str): arrival railway station
        start_month (int): first month of the selected period (included)
        end_month (int): last month of the selected period (included)
        historical_years (list[int]): past years selected for calculations,
            which should be available in the dataset
        data_df (pd.DataFrame): DataFrame containing the preprocessed data

    Returns:
        pd.DataFrame: A DataFrame containing one row per calendar month
            of the selected period, with the following columns:
                month : calendar month (1 to 12)
                minimum: minimum of monthly mean delay (minutes)
                q1: first quartile of monthly mean delay (minutes)
                median: median of monthly mean delay (minutes)
                q3: third quartile of monthly mean delay (minutes)
                maximum: maximum of monthly mean delay (minutes)
                number_historical_year_observations: number of
                    valid observations (historical years)
                sum_arr_delayed_trains: total number of delayed trains
                    associated with the valid monthly mean arrival delays
    """

    # prepare the list to store the statistics for each month
    # then calculate statistics for each selected month
    monthly_mean_delay_statistics = []

    for month in range(start_month, end_month + 1):
        statistics = calculate_mean_arrival_delay_distribution_per_month(
            departure_station, arrival_station, month, historical_years, data_df
        )

        # add the month to the statistics
        monthly_mean_delay_statistics.append(
            {
                "month": month,
                "minimum": statistics["minimum"],
                "q1": statistics["q1"],
                "median": statistics["median"],
                "q3": statistics["q3"],
                "maximum": statistics["maximum"],
                "number_historical_year_observations": statistics[
                    "number_historical_year_observations"
                ],
                "sum_arr_delayed_trains": statistics["sum_arr_delayed_trains"],
            }
        )

    # convert into a dataframe and return it
    monthly_mean_delay_distribution_df = pd.DataFrame(monthly_mean_delay_statistics)

    return monthly_mean_delay_distribution_df


def get_monthly_mean_arrival_delay_global_dataframe(
    departure_station: str,
    arrival_station: str,
    start_month: int,
    end_month: int,
    years_list: list[int],
    data_df: pd.DataFrame,
    actual_year: int = 2026,
) -> pd.DataFrame:
    """Generate a DataFrame combining historical statistics of mean arrival delays
        with the monthly mean arrival delays of the selected actual year,
        for a specific railway line and period of months.

        Historical statistics are calculated from the selected past years,
        excluding the actual year if present in the list.
        The actual year's observations are then added to the historical
        distribution for each calendar month.

        Months without valid observations from the actual year are kept
        in the DataFrame, with NaN values for the corresponding metrics.

    Args:
        departure_station (str): departure railway station
        arrival_station (str): arrival railway station
        start_month (int): first month of the selected period (included)
        end_month (int): last month of the selected period (included)
        years_list (list[int]): years selected for the historical calculations,
            excluding the actual year
        data_df (pd.DataFrame): DataFrame containing the preprocessed data
        actual_year (int, optional): year whose observations are compared
            with the historical distribution. Defaults to 2026.

    Returns:
        pd.DataFrame: a DataFrame containing one row per calendar month
            of the selected period, with the following columns:

            Historical statistics:
                month: calendar month (1 to 12)
                minimum: minimum of monthly mean arrival delay (minutes)
                q1: first quartile of monthly mean arrival delay (minutes)
                median: median of monthly mean arrival delay (minutes)
                q3: third quartile of monthly mean arrival delay (minutes)
                maximum: maximum of monthly mean arrival delay (minutes)
                number_historical_year_observations: number of valid
                    historical observations
                sum_arr_delayed_trains: total number of delayed trains
                    associated with valid historical monthly mean delays

            Actual year :
                mean_arrival_delay_actual_year: mean arrival delay (minutes)
                    for the corresponding month of the actual year
                number_arr_delayed_trains_actual_year: number of delayed trains
                    at arrival for the corresponding month of the actual year
    """

    # make a copy of the list of years and
    # delete the actual year from the list
    # to isolate past years
    historical_years = years_list.copy()

    if actual_year in historical_years:
        historical_years.remove(actual_year)

    # get the historical monthly distribution
    historical_mean_delay_distribution_df = (
        generate_historical_monthly_mean_arrival_delay_distribution_dataframe(
            departure_station,
            arrival_station,
            start_month,
            end_month,
            historical_years,
            data_df,
        )
    )

    # make the selection of the values for
    # the selected railway line
    df_stations = ld.get_filtered_departure_arrival_stations_df(
        departure_station, arrival_station, data_df
    )

    # generate dataframe with the observations of
    # the actual year
    actual_year_mean_delay_df = ld.get_filtered_period_df(
        start_month, end_month, [actual_year], df_stations
    )

    # rename the columns
    actual_year_mean_delay_df = actual_year_mean_delay_df[
        [
            ld.MONTH_KEY,
            ld.MEAN_ARRIVAL_DELAY_KEY,
            ld.MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY,
        ]
    ].rename(
        columns={
            ld.MONTH_KEY: "month",
            ld.MEAN_ARRIVAL_DELAY_KEY: "mean_arrival_delay_actual_year",
            ld.MONTHLY_DELAYED_ARRIVAL_TRAINS_KEY: (
                "number_arr_delayed_trains_actual_year"
            ),
        }
    )

    # drop invalid values
    actual_year_mean_delay_df = actual_year_mean_delay_df.dropna(
        subset=["mean_arrival_delay_actual_year"]
    )

    # merge historical statistics and actual year values
    global_mean_delay_df = historical_mean_delay_distribution_df.merge(
        actual_year_mean_delay_df, on="month", how="left", validate="one_to_one"
    )

    return global_mean_delay_df
